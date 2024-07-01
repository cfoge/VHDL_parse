library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use work.my_package.all;

entity my_entity is
    Port (
        clk : in  std_logic;
        rst : in  std_logic;
        input : in  integer;
        output : out  integer
    );
end my_entity;

architecture Behavioral of my_entity is
    signal my_signal : MY_TYPE;
begin
    process(clk, rst)
    begin
        if rst = '1' then
            output <= 0;
            my_signal.field1 <= '0';
            my_signal.field2 <= 0;
        elsif rising_edge(clk) then
            -- Use the constant and function from the package
            my_signal.field1 <= '1';
            my_signal.field2 <= MY_CONSTANT;
            output <= my_function(input);
        end if;
    end process;
end Behavioral;
