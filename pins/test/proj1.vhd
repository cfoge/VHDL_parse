library ieee;
use ieee.std_logic_1164.all;
--use ieee.std_logic_unsigned.all;
use ieee.numeric_std.all;

entity proj1 is
  port(
    f1_refclk0_n   : in std_logic;
    f1_refclk0_p   : in std_logic;
    f1_refclk1_n   : in std_logic;
    f1_refclk1_p   : in std_logic;
    lcd_refclk_n   : inout std_logic;
    eth_refclk_n   : inout std_logic;
    lcd_refclk_p   : inout std_logic;
    eth_refclk_p   : inout std_logic;
    in_vcxo_0_ctrl : out std_logic;
    in_vcxo_0_fs   : out std_logic;
    in_vcxo_1_ctrl : out std_logic;
    in_vcxo_1_fs   : out std_logic;
    lcd_data0_n    : out std_logic;
    lcd_data0_p    : out std_logic;
    lcd_data1_n    : out std_logic;
    lcd_data1_p    : out std_logic;
    lcd_data2_n    : out std_logic;
    lcd_data2_p    : out std_logic;
    lcd_data3_n    : out std_logic;
    lcd_data3_p    : out std_logic

  );
end entity;