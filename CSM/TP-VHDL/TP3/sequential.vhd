LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

PACKAGE bus_mux_pkg IS
	TYPE bus_mux_array IS ARRAY(NATURAL RANGE<>) OF STD_LOGIC_VECTOR(31 DOWNTO 0);
END PACKAGE bus_mux_pkg;

-------------------------------------------------

-- Register

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity Reg is
  	PORT(
    source: in std_logic_vector(31 downto 0);
    output : out std_logic_vector(31 downto 0);
    wr, clk : in std_logic
    );
end entity;

architecture arch_Reg of Reg is
begin

P_REG32: process(clk)
begin
	if(rising_edge(clk)) then
		if(wr='1') then 
			output <= source;
		end if;
	end if;
end process P_REG32;

end arch_Reg;
-------------------------------------------------

-- Register bank

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
USE work.bus_mux_pkg.ALL;

ENTITY RegisterBank IS
	PORT
	(
		s_reg_0 	: in std_logic_vector(4 DOWNTO 0);
		data_o_0 	: out std_logic_vector(31 DOWNTO 0); 
		s_reg_1 	: in std_logic_vector(4 DOWNTO 0);
		data_o_1 	: out std_logic_vector(31 DOWNTO 0);
		dest_reg 	: in std_logic_vector(4 DOWNTO 0);
		data_i 		: in std_logic_vector(31 DOWNTO 0);
		wr_reg 		: in std_logic;
		clk 		: in std_logic
	);
END ENTITY RegisterBank;

architecture arch_BankReg of RegisterBank is
	signal REGS : bus_mux_array(31 downto 0);

begin

data_o_0 <= REGS(to_integer(unsigned(s_reg_0))) WHEN s_reg_0 /= std_logic_vector(to_unsigned(0,5)) else
	(others => '0');
data_o_1 <= REGS(to_integer(unsigned(s_reg_1))) WHEN s_reg_1 /= std_logic_vector(to_unsigned(0,5)) else
	(others => '0');

P_REG32: process(clk)
begin
	if(rising_edge(clk)) then 
		if(wr_reg='1') then
			REGS(to_integer(unsigned(dest_reg))) <= data_i;
		end if;
	end if;
end process P_REG32;

end arch_BankReg;