library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

package my_package is

    -- Define a constant
    constant MY_CONSTANT : integer := 42;

    -- Define a type
    type MY_TYPE is record
        field1 : std_logic;
        field2 : integer;
    end record;

    -- Declare a function
    function my_function(input : integer) return integer;

end my_package;
