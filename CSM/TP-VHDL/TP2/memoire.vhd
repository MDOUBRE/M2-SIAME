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


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity Ecriture is
    PORT(
    address, data_in, current_mem : in std_logic_vector(31 downto 0);
    data_out    : out std_logic_vector(31 downto 0);
    WriteMem_W, WriteMem_H, WriteMem_B : in std_logic
    );
end entity;

architecture arch_Ecriture of Ecriture is
    signal demi0, demi1 : std_logic_vector(31 downto 0);
    signal octet0, octet1, octet2, octet3 : std_logic_vector(31 downto 0);
begin
    demi0 <= current_mem(31 downto 16) & data_in(15 downto 0);
    demi1 <= current_mem(31 downto 16) & data_in(31 downto 16);
    octet0 <= current_mem(31 downto 8) & data_in(7 downto 0);
    octet1 <= current_mem(31 downto 8) & data_in(15 downto 8);
    octet2 <= current_mem(31 downto 8) & data_in(23 downto 16);
    octet3 <= current_mem(31 downto 8) & data_in(31 downto 24);

    data_out <= data_in when WriteMem_W = '1' else
                demi0 when WriteMem_H = '1' and address(0) = '0' else 
                demi1 when WriteMem_H = '1' and address(0) = '1' else 
                octet0 when WriteMem_B = '1' and address(1 downto 0) = "00" else
                octet1 when WriteMem_B = '1' and address(1 downto 0) = "01" else
                octet2 when WriteMem_B = '1' and address(1 downto 0) = "10" else
                octet3 when WriteMem_B = '1' and address(1 downto 0) = "11";

end arch_Ecriture;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity memoire is
    port(
    address, data_in, current_mem : in std_logic_vector(31 downto 0);
    data_out : out std_logic_vector(31 downto 0);
    ReadMem_W, ReadMem_SH, ReadMem_UH, ReadMem_SB, ReadMem_UB : in std_logic;
    WriteMem_W, WriteMem_H, WriteMem_B : in std_logic;
    WE, OE, clk : in std_logic
    );
end entity;

architecture arch_memoire of memoire is
    type tab2048x32 is array(2047 downto 0) of std_logic_vector(31 downto 0);
    signal tab : tab2048x32;
    signal mot,data_write, data_read: std_logic_vector(31 downto 0);
begin
    mot <= tab(to_integer(unsigned(address)));
    read : Entity work.lecture port map (address, mot, data_read, ReadMem_W, ReadMem_SH, ReadMem_UH, ReadMem_SB, ReadMem_UB);
    write : Entity work.ecriture port map (address, data_in, mot, data_write, WriteMem_W, WriteMem_H, WriteMem_B);

P_ALU : process(CLK)

    begin
    if rising_edge(CLK) then
        if (WE = '1') then
            data_out <= data_read;
        else 
            tab(to_integer(unsigned(address))) <= data_write;
            data_out <= data_write;
        end if; 

        if (OE = '1') then
            data_out <= (others => 'Z');
        end if;
    end if;
end process P_ALU;   

end arch_memoire;