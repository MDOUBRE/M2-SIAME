
----------------------------------------------

-- Mux 4->1

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity mux4_1 is
  generic (size : integer);
  port(
    reg0, reg1, reg2, reg3 : in std_logic_vector(size-1 downto 0);
    reg_out : out std_logic_vector(size-1 downto 0);
    c : in std_logic_vector(1 downto 0)
    );
end entity;

architecture multiplexeur of mux4_1 is
begin

reg_out <= reg0 WHEN c = "00" else
           reg1 WHEN c = "01" else
           reg2 WHEN c = "10" else
           reg3;
          
end multiplexeur;

----------------------------------------------------

--Simple adder for 32 bit words

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity add is
  port(
    reg1, reg2 : in std_logic_vector(31 downto 0);
    reg3 : out std_logic_vector(31 downto 0)
    );
end entity;

architecture additionneur of add is
begin

reg3 <= std_logic_vector(unsigned(reg1) + unsigned(reg2));  

end additionneur;

------------------------------------------------------

-- Full 32b adder with carry bits out
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity addCarry1 is
  port(
    A, B, cin: in std_logic;
    s, cout: out std_logic);
end entity;

architecture addRet1 of addCarry1 is
begin

  s <= (A xor B) xor cin;
  cout <= (A and B) or (A and cin) or (B and cin);

end addRet1;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity addCarry is
  port(
    A, B: in std_logic_vector(31 downto 0);
    cin: in std_logic;
    s : out std_logic_vector(31 downto 0);
    c30, c31: out std_logic);
end entity;

architecture additionneurRetenue of addCarry is

  signal c : std_logic_vector(32 downto 0);

begin
  c(0) <= cin;
  c30 <= c(31);
  c31 <= c(32);

  G : for i in 0 to 31 generate
    inst : entity work.addCarry1 port map(A(i), B(i), c(i), s(i), c(i+1));
  end generate;

end additionneurRetenue;

-----------------------------------------------

-- Barrel shifter

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
use work.bus_mux_pkg.ALL;

entity BarrelShifter IS
  port (
    A : in std_logic_vector(31 downto 0);
    ValDec : in std_logic_vector(4 downto 0);
    SR, SL : out std_logic_vector(31 downto 0)
    );
end entity;

architecture barrelShift of BarrelShifter is

  signal tab : std_logic_vector(95 downto 0);

begin

  g1 : for i in 0 to 31 generate  
    tab(i) <= '0';
  end generate;
  g2 : for i in 32 to 63 generate
    tab(i) <= A(i-32);
  end generate;
  g3 : for i in 64 to 95 generate
    tab(i) <= '0';
  end generate;

  g4 : for i in 32 to 63 generate
    SL(i-32) <= tab(i-to_integer(unsigned(ValDec)));
  end generate;
  g5 : for i in 32 to 63 generate
    SR(i-32) <= tab(i+to_integer(unsigned(ValDec)));
  end generate;

end barrelShift;

---------------------------------------------------

-- Full ALU

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

ENTITY ALU IS
	PORT
	(
		A : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
		B : IN STD_LOGIC_VECTOR(31 DOWNTO 0);
		sel : IN STD_LOGIC_VECTOR(3 DOWNTO 0);
		Enable_V : IN STD_LOGIC;
		ValDec : IN STD_LOGIC_VECTOR(4 DOWNTO 0);
		Slt : IN STD_LOGIC;
		CLK : IN STD_LOGIC;
		Res : OUT STD_LOGIC_VECTOR(31 DOWNTO 0);
		N : OUT STD_LOGIC;
		Z : OUT STD_LOGIC;
		C : OUT STD_LOGIC;
		V : OUT STD_LOGIC
	);
END ENTITY ALU;

---------------------------------------------------

-- Extension logic for immediate inputs

LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity extension is
  port(
    inst : in std_logic_vector(31 downto 0);
    ExtOp : in std_logic;
    ExtOut : out std_logic_vector(31 downto 0)
    );
end entity;
