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

begin


    end arch_Ecriture;