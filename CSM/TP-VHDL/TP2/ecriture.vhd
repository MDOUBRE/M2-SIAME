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