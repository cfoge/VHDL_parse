-------------------------------------------------------------------------------
-- fan_control.vhd
-- 
-- Author               : Neil SHI, Anton S
-- Created              : 20/08/2019 / 28/12/2022
-------------------------------------------------------------------------------
-- Simple fan control to compromise FPGA temp with noise
-- Use simple averaging to smooth the fan speed change
-- XADC value vs Temp(C) is as following
--
-- 7 series:
-- XADC =(Temp+273.15)*2^12/503.975
-- Temp =(XADC*503.975/2^12)-273.15
-- 
-- Ultrascale:
-- XADC =(Temp+280.23)*2^12/509.314
-- Temp =(XADC*509.314/2^12)-280.23
-- 
-- If using both Ultrascale and 7 series, a conversion by adding a fixed
-- offset is used.
-------------------------------------------------------------------------------
library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.NUMERIC_STD.ALL;

library UNISIM;
use UNISIM.VCOMPONENTS.all;

entity fan_control is
generic (
    FAN_ON_STATE     : std_logic  := '1';  -- Defines whether FAN_ON is active high or low
    PWM_MIN          : integer    := 200;  -- ~20%, Min PWM duty cycle (/1024)
    PWM_MAX          : integer    := 1023; -- ~100%, Max PWM duty cycle (/1024)
    TEMP_PWM_MIN_C   : real       := 65.0; -- 65C;  
    TEMP_PWM_MAX_C   : real       := 95.0; -- 95C;  
    TEMP_FORMULA     : integer    := 0;    -- Use XADC transfer function for 7-series (0), or SysMone4 function for Ultrascale+(1)
    USE_DSP48        : boolean    := FALSE
);
port (
    clk             : in  std_logic;
    refclk_10ms_stb : in  std_logic;        -- single clock width pulse with cycle time of 10mS

    -- Interface with fan and XADC
    temp1_in        : in  std_logic_vector(11 downto 0);
    temp2_in        : in  std_logic_vector(11 downto 0);
    temp3_in        : in  std_logic_vector(11 downto 0);
    temp4_in        : in  std_logic_vector(11 downto 0);
    temp5_in        : in  std_logic_vector(11 downto 0);
    temp6_in        : in  std_logic_vector(11 downto 0);
    temp7_in        : in  std_logic_vector(11 downto 0);
    
    fan1_sens       : in  std_logic;
    fan2_sens       : in  std_logic;
    fan3_sens       : in  std_logic;
    fan4_sens       : in  std_logic;
    
    fan_ctrl        : out std_logic;

    -- interface with software
    fan1_spd_out    : out std_logic_vector(15 downto 0);
    fan2_spd_out    : out std_logic_vector(15 downto 0);
    fan3_spd_out    : out std_logic_vector(15 downto 0);
    fan4_spd_out    : out std_logic_vector(15 downto 0);
    
    fan_pwm_out     : out std_logic_vector(15 downto 0);
    fan_force_pwm   : in  std_logic;
    fan_pwm_in      : in  std_logic_vector(15 downto 0);
    
    debug_clk       : out std_logic;
    debug           : out std_logic_vector(127 downto 0)
);
end entity;

architecture rtl of fan_control is

signal pwm_gen             : std_logic_vector(24 downto 0);
signal pwm_set             : unsigned(9 downto 0);
signal pwm_lat             : unsigned(9 downto 0);
signal pwm_lut             : std_logic_vector(23 downto 0);
signal pwm_lut_d           : std_logic_vector(11 downto 0);
signal pwm_cur             : unsigned(9 downto 0) := to_unsigned(PWM_MIN,10);
signal pwm_delta_up        : unsigned(9 downto 0);
signal pwm_delta_dn        : unsigned(9 downto 0);
signal pwm_delta_up_step   : unsigned(9 downto 0);
signal pwm_delta_dn_step   : unsigned(9 downto 0);
signal pwm_value_mux       : unsigned(9 downto 0);
signal pwm_cnt             : unsigned(9 downto 0)         := to_unsigned(0, 10);

signal stb_1s              : std_logic                    := '0';

signal fan1_sens_samples   : std_logic_vector(2 downto 0) := "000";
signal fan2_sens_samples   : std_logic_vector(2 downto 0) := "000";
signal fan3_sens_samples   : std_logic_vector(2 downto 0) := "000";
signal fan4_sens_samples   : std_logic_vector(2 downto 0) := "000";

signal f1_tacho_pulse      : std_logic;
signal f2_tacho_pulse      : std_logic;
signal f3_tacho_pulse      : std_logic;
signal f4_tacho_pulse      : std_logic;
signal f5_tacho_pulse      : std_logic;
signal f6_tacho_pulse      : std_logic;
signal f7_tacho_pulse      : std_logic;

signal fan1_spd            : unsigned(9 downto 0);
signal fan2_spd            : unsigned(9 downto 0);
signal fan3_spd            : unsigned(9 downto 0);
signal fan4_spd            : unsigned(9 downto 0);

signal cnt_fan1            : unsigned(9 downto 0);
signal cnt_fan2            : unsigned(9 downto 0);
signal cnt_fan3            : unsigned(9 downto 0);
signal cnt_fan4            : unsigned(9 downto 0);

-- 7 series:
-- XADC =(Temp+273.15)*2^12/503.975
-- Temp =(XADC*503.975/2^12)-273.15
-- 
-- Ultrascale:
-- XADC =(Temp+280.23)*2^12/509.314
-- Temp =(XADC*509.314/2^12)-280.23

function get_temp(temp_c : real :=0.0; sel_formula : integer := 0) return integer is
begin
    if (sel_formula=0) then -- Use 7-series XADC conversion formula
        return integer((temp_c+273.15)*4096.0/503.975);
    elsif (sel_formula=1) then -- Use Ultrascale SysMonE4 conversion formula
        return integer((temp_c+280.23)*4096.0/509.314);
    else
        return 0;
    end if;
end function;

constant TEMP_PWM_MIN : integer := get_temp(TEMP_PWM_MIN_C,TEMP_FORMULA);
constant TEMP_PWM_MAX : integer := get_temp(TEMP_PWM_MAX_C,TEMP_FORMULA);

constant PWM_SLOPE    : integer := (PWM_MAX-PWM_MIN)/(TEMP_PWM_MAX-TEMP_PWM_MIN);

constant TEMP_AVG          : integer := 7; -- 2^7 samples averaging
constant PWM_AVG_UP        : integer := 8; -- 255*10ms  ~ 2s
constant PWM_AVG_DN        : integer := 9; -- 511*10ms  ~ 5s

signal temp                : unsigned(11 downto 0);
signal temp_acc            : unsigned(12+TEMP_AVG-1 downto 0):=(others =>'0');
signal temp_cnt            : unsigned(TEMP_AVG-1 downto 0):=(others =>'0');
signal temp_reg            : unsigned(11 downto 0):=(others =>'0');
signal temp_delta          : unsigned(11 downto 0):=(others =>'0');

signal temp1_reg           : unsigned(11 downto 0);
signal temp2_reg           : unsigned(11 downto 0);
signal temp3_reg           : unsigned(11 downto 0);
signal temp4_reg           : unsigned(11 downto 0);
signal temp5_reg           : unsigned(11 downto 0);
signal temp6_reg           : unsigned(11 downto 0);
signal temp7_reg           : unsigned(11 downto 0);

signal temp_cmp1           : unsigned(11 downto 0);
signal temp_cmp2           : unsigned(11 downto 0);
signal temp_cmp3           : unsigned(11 downto 0);
signal temp_cmp4           : unsigned(11 downto 0);
signal temp_cmp5           : unsigned(11 downto 0);
signal temp_cmp6           : unsigned(11 downto 0);
signal temp_cmp7           : unsigned(11 downto 0);

signal cnt_3s              : unsigned(3 downto 0);
signal ref10ms_cnt         : unsigned(7 downto 0);

begin

-- Generate a 1 second strobe
process (clk)
begin
if rising_edge(clk) then
    if refclk_10ms_stb = '1' then
        if (ref10ms_cnt = to_unsigned(99,8)) then 
            ref10ms_cnt <= (others=>'0');
            stb_1s      <= '1';
        else
            ref10ms_cnt <= ref10ms_cnt+1;
            stb_1s      <= '0';
        end if;
    else
        stb_1s <= '0';
    end if;
end if;
end process;

-- Condition the input temperatures: lock in the register, reject 0xFFF, and choose the highest
temp_regsters: process(clk)
begin
if rising_edge(clk) then
    temp1_reg <= unsigned(temp1_in);
    temp2_reg <= unsigned(temp2_in);
    temp3_reg <= unsigned(temp3_in);
    temp4_reg <= unsigned(temp4_in);
    temp5_reg <= unsigned(temp5_in);
    temp6_reg <= unsigned(temp6_in); -- +to_unsigned(27,12); -- FPGA6 is 7-series, use offset to convert temp
    temp7_reg <= unsigned(temp7_in); -- +to_unsigned(27,12); -- FPGA7 is 7-series, use offset to convert temp
    
    temp      <= temp_cmp7;
end if;
end process;

temp_cmp1 <= temp1_reg when (temp1_reg > temp2_reg) and (temp1_reg/=x"FFF") else temp2_reg;
temp_cmp2 <= temp3_reg when (temp3_reg > temp4_reg) and (temp3_reg/=x"FFF") else temp4_reg;
temp_cmp3 <= temp5_reg when (temp5_reg > temp6_reg) and (temp5_reg/=x"FFF") else temp6_reg;
temp_cmp4 <= temp7_reg;

temp_cmp5 <= temp_cmp1 when (temp_cmp1 > temp_cmp2) and (temp_cmp1/=x"FFF") else temp_cmp2;
temp_cmp6 <= temp_cmp3 when (temp_cmp3 > temp_cmp4) and (temp_cmp3/=x"FFF") else temp_cmp4;

temp_cmp7 <= temp_cmp5 when (temp_cmp5 > temp_cmp6) and (temp_cmp5/=x"FFF") else temp_cmp6;

ave_temp : process(clk)
begin
  if (rising_edge(clk)) then

    -- Filter the temperature signal, simple averaging over 2^TEMP_AVG samples, non-sliding window
    if (refclk_10ms_stb='1') then
        if (temp_cnt=0) then
            temp_reg <= temp_acc(12-1+TEMP_AVG downto 0+TEMP_AVG);
            temp_acc <= resize(temp,12+TEMP_AVG);
            temp_cnt <= temp_cnt+1;
        else
            temp_reg <= temp_reg;
            temp_acc <= temp_acc+resize(temp,12+TEMP_AVG);
            temp_cnt <= temp_cnt+1;
        end if;
    end if;
  end if;
end process;

-- The curve
-- pwm = PWM_MIN                             when T < TEMP_PWM_MIN
--       PWM_SLOPE*(T-TEMP_PWM_MIN)+PWM_MIN  when T = (TEMP_PWM_MIN..TEMP_PWM_MAX)
--       PWM_MAX                             when T > TEMP_PWM_MAX

-- use DSP (D-A)*B+C
PWM_DSP_GEN: if USE_DSP48=TRUE generate 
pwm_dsp_i : entity work.fc_pwm_dsp
port map (
  CLK    => clk,
  A      => std_logic_vector(to_unsigned(TEMP_PWM_MIN,12)),
  B      => std_logic_vector(to_unsigned(PWM_SLOPE,12)),
  C      => std_logic_vector(to_unsigned(PWM_MIN,12)),
  D      => std_logic_vector(temp_reg),
  P      => pwm_gen
);
end generate PWM_DSP_GEN;

-- use LUTs for multiplier
PWM_LUT_GEN: if USE_DSP48=FALSE generate 
process(clk)
begin
  if (rising_edge(clk)) then
    temp_delta <= temp_reg - to_unsigned(TEMP_PWM_MIN,12); -- temp_delta = T-TEMP_PWM_MIN
    pwm_lut_d  <= pwm_lut(11 downto 0);                    -- pwm_lut    = temp_delta*PWM_SLOPE
    pwm_gen(11 downto 0) <= std_logic_vector(unsigned(pwm_lut_d) + to_unsigned(PWM_MIN,12)); -- pwm_gen = pwm_lut_d + PWM_MIN
  end if;
end process;

pwm_lut_i : entity work.fc_pwm_lut
port map(
  CLK    => clk,
  A      => std_logic_vector(temp_delta),
  B      => std_logic_vector(to_unsigned(PWM_SLOPE,12)),
  P      => pwm_lut
);
end generate PWM_LUT_GEN;

-- pwm set by current temp
process(clk)
begin
  if (rising_edge(clk)) then
    if temp_reg < to_unsigned(TEMP_PWM_MIN,temp_reg'length) then
      pwm_set <= to_unsigned(PWM_MIN,pwm_set'length);
    elsif temp_reg > to_unsigned(TEMP_PWM_MAX,temp_reg'length) then
      pwm_set <= to_unsigned(PWM_MAX,pwm_set'length);
    else
      pwm_set <= unsigned(pwm_gen(9 downto 0));
    end if;
  end if;
end process;

process(clk)
begin
  if (rising_edge(clk)) then
    if (temp_cnt=0) then
      pwm_delta_up <= pwm_set - pwm_cur;
      pwm_delta_dn <= pwm_cur - pwm_set;
    end if;
  end if;
end process;

pwm_delta_up_step <= to_unsigned(1, pwm_delta_up_step'length) when pwm_delta_up(pwm_delta_up'high downto PWM_AVG_UP) = 0 else
                     ((pwm_delta_up'high downto pwm_delta_up'high-PWM_AVG_UP+1  => '0') & pwm_delta_up(pwm_delta_up'high downto PWM_AVG_UP));

pwm_delta_dn_step <= to_unsigned(1, pwm_delta_dn_step'length) when pwm_delta_dn(pwm_delta_dn'high downto PWM_AVG_dn) = 0 else
                     ((pwm_delta_dn'high downto pwm_delta_dn'high-PWM_AVG_DN+1  => '0') & pwm_delta_dn(pwm_delta_dn'high downto PWM_AVG_DN));

process(clk)
begin
  if (rising_edge(clk)) then
    if (refclk_10ms_stb='1') then
      if pwm_set > pwm_cur then
        pwm_cur <= pwm_cur + pwm_delta_up_step;
      elsif pwm_set < pwm_cur then
        pwm_cur <= pwm_cur - pwm_delta_dn_step;
      end if;
    end if;
  end if;
end process;

-- sw override
process(clk)
begin
  if (rising_edge(clk)) then
    if fan_force_pwm = '1' then
      pwm_value_mux <= unsigned(fan_pwm_in(9 downto 0));
    elsif temp_reg > to_unsigned(TEMP_PWM_MAX,temp_reg'length) then
      pwm_value_mux <= to_unsigned(PWM_MAX,pwm_value_mux'length);
    else
      pwm_value_mux <= pwm_cur(9 downto 0);
    end if;
end if;
end process;

fan_pwm_out(9 downto 0) <= std_logic_vector(pwm_value_mux);

----------------------------------------------------------------------------------------------------------------------------------------
-- fpga fan control
--
-- PWM counter counts modulo 1024 to obtain a 23.4375kHz 
-- 
-----------------------------------------------------------------------------------------------------------------------------------------
generate_pwm : process(clk) 
begin
if rising_edge(clk) then
    if (pwm_cnt > pwm_value_mux) then fan_ctrl <= not FAN_ON_STATE;
    else                              fan_ctrl <= FAN_ON_STATE;
    end if;
    if (pwm_cnt < to_unsigned(PWM_MAX,pwm_cnt'length))  then    pwm_cnt <= pwm_cnt + 1;
    else                            pwm_cnt <= to_unsigned(0, 10);      -- PWM frequency is 23.4375kHz 
    end if;
end if;
end process;

------------------------------------------------------------------------------------------------------------------------------------------
-- fpga fan monitor 
------------------------------------------------------------------------------------------------------------------------------------------

-- Fan speed counter
fan_spd_mon: process(clk)
begin
if rising_edge(clk) then
    fan1_sens_samples <= fan1_sens_samples(1 downto 0) &  fan1_sens;    -- retime for synchronization and edge detect
    fan2_sens_samples <= fan2_sens_samples(1 downto 0) &  fan2_sens;    -- retime for synchronization and edge detect
    fan3_sens_samples <= fan3_sens_samples(1 downto 0) &  fan3_sens;    -- retime for synchronization and edge detect
    fan4_sens_samples <= fan4_sens_samples(1 downto 0) &  fan4_sens;    -- retime for synchronization and edge detect
    
    if (fan1_sens_samples(2 downto 1) = "01") then f1_tacho_pulse <= '1'; else f1_tacho_pulse <= '0'; end if;
    if (fan2_sens_samples(2 downto 1) = "01") then f2_tacho_pulse <= '1'; else f2_tacho_pulse <= '0'; end if;
    if (fan3_sens_samples(2 downto 1) = "01") then f3_tacho_pulse <= '1'; else f3_tacho_pulse <= '0'; end if;
    if (fan4_sens_samples(2 downto 1) = "01") then f4_tacho_pulse <= '1'; else f4_tacho_pulse <= '0'; end if;
  
    -- Calculate the number of pulses at 3 seconds; 2 pulses per rev;
    -- at 3 seconds it will give us the number of full revs per 6 seconds; that'd be RPM divided by 10
    if (stb_1s='1') then
        if (cnt_3s=to_unsigned(2,4)) then
            cnt_3s   <= (others=>'0');
            
            fan1_spd <= cnt_fan1;
            fan2_spd <= cnt_fan2;
            fan3_spd <= cnt_fan3;
            fan4_spd <= cnt_fan4;
            
            cnt_fan1 <= (others=>'0');
            cnt_fan2 <= (others=>'0');
            cnt_fan3 <= (others=>'0');
            cnt_fan4 <= (others=>'0');
        else
            cnt_3s <= cnt_3s+1;
            
            if (f1_tacho_pulse='1') then cnt_fan1 <= cnt_fan1+1; end if;
            if (f2_tacho_pulse='1') then cnt_fan2 <= cnt_fan2+1; end if;
            if (f3_tacho_pulse='1') then cnt_fan3 <= cnt_fan3+1; end if;
            if (f4_tacho_pulse='1') then cnt_fan4 <= cnt_fan4+1; end if;
        end if;
    else
        if (f1_tacho_pulse='1') then cnt_fan1 <= cnt_fan1+1; end if;
        if (f2_tacho_pulse='1') then cnt_fan2 <= cnt_fan2+1; end if;
        if (f3_tacho_pulse='1') then cnt_fan3 <= cnt_fan3+1; end if;
        if (f4_tacho_pulse='1') then cnt_fan4 <= cnt_fan4+1; end if;
    end if;
    
end if;
end process;

fan1_spd_out <= std_logic_vector(resize(fan1_spd,16));
fan2_spd_out <= std_logic_vector(resize(fan2_spd,16));
fan3_spd_out <= std_logic_vector(resize(fan3_spd,16));
fan4_spd_out <= std_logic_vector(resize(fan4_spd,16));

debug_clk           <= clk;
--
debug(11 downto 0)  <= std_logic_vector(temp);
debug(23 downto 12) <= std_logic_vector(temp_reg);
debug(33 downto 24) <= std_logic_vector(pwm_delta_up);
debug(43 downto 34) <= std_logic_vector(pwm_delta_dn);
debug(53 downto 44) <= std_logic_vector(pwm_set);
debug(63 downto 54) <= std_logic_vector(pwm_cur);
debug(73 downto 64) <= std_logic_vector(pwm_gen(9 downto 0));
debug(83 downto 74) <= std_logic_vector(pwm_value_mux);
debug(99 downto 84) <= std_logic_vector(resize(fan1_spd,16));

-- Below is to report the calculated threshold in the synth log
-- Be sure to enable the assertions in Vivado using -assert switch
-- when calling synth_design in the TCL script 
assert FALSE report "TEMP_PWM_MIN = " & integer'image(TEMP_PWM_MIN) severity NOTE;
assert FALSE report "TEMP_PWM_MAX = " & integer'image(TEMP_PWM_MAX) severity NOTE;

--
---- debug(95 downto 80) <= std_logic_vector(cnt_fan1);
---- debug(96)           <= f1_tacho_pulse;
---- debug(97)           <= fan1_sens;
--
--debug(127 downto 120) <= std_logic_vector(ref10ms_cnt);
--debug(110+TEMP_AVG-1 downto 110) <= std_logic_vector(temp_cnt);
--debug(108)            <= refclk_10ms_stb;
--debug(109)            <= stb_1s;

--  debug(9 downto 0) <= std_logic_vector(pwm_value);
--  debug(19 downto 10) <= (others => '0');
--  debug(20) <= stb_100ms;
--  debug(21) <= fan1_fail_int;
--  debug(43 downto 23) <= (others => '0');

end architecture;
