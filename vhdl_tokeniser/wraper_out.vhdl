--Auto generated VHDL Wrapper
LIBRARY ieee; 
USE ieee.std_logic_1164.all; 

entity {wrapper_name} is 
clock : in std_logic; 
A : in std_logic_vector(7 downto 0); 
B : in std_logic_vector(7 downto 0); 
IAB : in std_logic; 
Output : out std_logic; 
end wrapper_test; 

architecture rtl of wrapper_test is 
 Full_Adder_Structural_VHDL_i : entity work.Full_Adder_Structural_VHDL 
port map (
X1      => X1, --in width = std_logic
X2      => X2, --in width = std_logic
Cin     => Cin, --in width = std_logic
S       => S, --out width = std_logic
Cout    => Cout --out width = std_logic
);

end rtl; 
