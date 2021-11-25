LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity Lecture is
    PORT(
    address, Read_in : in std_logic_vector(31 downto 0);
    Read_out    : out std_logic_vector(31 downto 0);
    ReadMem_W, ReadMem_SH, ReadMem_UH, ReadMem_SB, ReadMem_UB : in std_logic
    );
end entity;
  
architecture arch_Lecture of Lecture is
    signal demi0, demi0S, demi1, demi1S : std_logic_vector(31 downto 0);
    signal octet0, octet1, octet2, octet3 : std_logic_vector(31 downto 0);
    signal octet0S, octet1S, octet2S, octet3S : std_logic_vector(31 downto 0);
begin

demi0(31 downto 16) <= (others => '0');    
demi0(15 downto 0) <= Read_in(15 downto 0);
demi0S(31 downto 16) <= (others => Read_in(15));    
demi0S(15 downto 0) <= Read_in(15 downto 0);

demi1(31 downto 16) <= (others => '0');    
demi1(15 downto 0) <= Read_in(31 downto 16);
demi1S(31 downto 16) <= (others => Read_in(31));    
demi1S(15 downto 0) <= Read_in(31 downto 16);

octet0(31 downto 8) <= (others => '0');
octet0(7 downto 0) <= Read_in(7 downto 0);
octet0S(31 downto 8) <= (others => Read_in(7));
octet0S(7 downto 0) <= Read_in(7 downto 0);

octet1(31 downto 8) <= (others => '0');
octet1(7 downto 0) <= Read_in(15 downto 8);
octet1S(31 downto 8) <= (others => Read_in(15));
octet1S(7 downto 0) <= Read_in(15 downto 8);

octet2(31 downto 8) <= (others => '0');
octet2(7 downto 0) <= Read_in(23 downto 16);
octet2S(31 downto 8) <= (others => Read_in(23));
octet2S(7 downto 0) <= Read_in(23 downto 16);

octet3(31 downto 8) <= (others => '0');
octet3(7 downto 0) <= Read_in(31 downto 24);
octet3S(31 downto 8) <= (others => Read_in(31));
octet3S(7 downto 0) <= Read_in(31 downto 24);


Read_out <= Read_in when ReadMem_W = '1'else
            demi0S when (ReadMem_SH = '1' and address(1 downto 0) = "00") else
            demi0 when (ReadMem_UH = '1' and address(1 downto 0) = "00") else
            demi1S when (ReadMem_SH = '1' and address(1 downto 0) = "10") else
            demi1 when (ReadMem_UH = '1' and address(1 downto 0) = "10") else
            octet0S when (ReadMem_SB = '1' and address(1 downto 0) = "00") else
            octet0 when (ReadMem_UB = '1' and address(1 downto 0) = "00") else
            octet1S when (ReadMem_SB = '1' and address(1 downto 0) = "01") else
            octet1 when (ReadMem_UB = '1' and address(1 downto 0) = "01") else
            octet2S when (ReadMem_SB = '1' and address(1 downto 0) = "10") else
            octet2 when (ReadMem_UB = '1' and address(1 downto 0) = "10") else
            octet3S when (ReadMem_SB = '1' and address(1 downto 0) = "11") else
            octet3 when (ReadMem_UB = '1' and address(1 downto 0) = "11") else
            (others => 'X');

end arch_Lecture;