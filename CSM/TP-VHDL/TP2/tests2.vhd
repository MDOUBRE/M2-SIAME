LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_Lecture is
end test_Lecture;

architecture arch_test_Lecture of test_Lecture is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

signal E_address, E_Read_in, E_Read_out : std_logic_vector(31 downto 0);
signal E_ReadMem_W, E_ReadMem_SH, E_ReadMem_UH, E_ReadMem_SB, E_ReadMem_UB : std_logic;

begin 

regf0 : entity work.Lecture
    port map (address => E_address,
                Read_in => E_Read_in,
                Read_out => E_Read_out,
                ReadMem_W => E_ReadMem_W, 
                ReadMem_SH => E_ReadMem_SH, 
                ReadMem_UH => E_ReadMem_UH, 
                ReadMem_SB => E_ReadMem_SB, 
                ReadMem_UB => E_ReadMem_UB);        

P_LECTURE_TEST: process
begin
    E_ReadMem_SB <= '0';
    E_ReadMem_UB <= '0';
    E_ReadMem_SH <= '0';
    E_ReadMem_UH <= '0';
    E_Read_in <= "10110100010110010110100110010110";
    E_address(1 downto 0) <= "00";
    
    E_ReadMem_SB <= '1';
    wait for clkpulse; 

    E_ReadMem_SB <= '0';
    E_ReadMem_UB <= '1';
    wait for clkpulse; 

    E_address(1 downto 0) <= "10";
    E_ReadMem_UB <= '0';
    E_ReadMem_SH <= '1';
    wait for clkpulse; 

    E_ReadMem_SH <= '0';
    E_ReadMem_UH <= '1';
    wait for clkpulse; 

    E_address(1 downto 0) <= "01";
    wait for clkpulse; 

    E_address(1 downto 0) <= "01";
    E_ReadMem_UH <= '0';
    E_ReadMem_SB <= '1';
    wait for clkpulse;
    wait;

end process P_LECTURE_TEST;

end arch_test_Lecture;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;
    
entity test_ecriture is
end test_ecriture;
    
architecture arch_lecture of test_ecriture is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

-- definition de ressources externes
signal E_address, E_data_in, E_current_mem : std_logic_vector(31 downto 0);
signal E_data_out : std_logic_vector(31 downto 0);
signal E_WriteMem_W, E_WriteMem_H, E_WriteMem_B: std_logic;
    
begin

regf0 : entity work.ecriture(arch_ecriture)
    port map(address => E_address,
                data_in => E_data_in,
                current_mem => E_current_mem,
                data_out => E_data_out,
                WriteMem_W => E_WriteMem_W,
                WriteMem_H => E_WriteMem_H,
                WriteMem_B => E_WriteMem_B);
    
P_ECRITURE_TEST: process
begin   
    E_address <= (others => '0');
    E_WriteMem_W <= '1';
    E_WriteMem_H <= '0';  
    E_WriteMem_B <= '0';
    E_data_in <= "11111111111010101010111111101110";
    E_current_mem <= "00000000000000000000000000000000";    
    wait for clkpulse;

    E_WriteMem_W <= '0';
    E_WriteMem_H <= '1';     
    wait for clkpulse;

    E_address <= (0 => '1', others => '0');    
    E_WriteMem_H <= '0';
    E_WriteMem_B <= '1';    
    wait for clkpulse;        
    wait;

end process P_ECRITURE_TEST;

end arch_lecture;
       
    
LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

-- Definition de l'entite
entity test_memoire is
end test_memoire;
    
-- Definition de l'architecture
architecture arch_memoire of test_memoire is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

-- definition de ressources externes
signal E_address, E_data_in: std_logic_vector(31 downto 0);
signal E_data_out : std_logic_vector(31 downto 0);
signal E_ReadMem_W, E_ReadMem_SH, E_ReadMem_UH, E_ReadMem_SB, E_ReadMem_UB, E_WriteMem_W, E_WriteMem_H, E_WriteMem_B, E_WE, E_OE, E_clk : std_logic;

begin

regf0 : entity work.memoire(arch_memoire)
    port map(address => E_address,
                data_in => E_data_in,
                data_out => E_data_out,
                ReadMem_W => E_ReadMem_W,
                ReadMem_SH => E_ReadMem_SH,
                ReadMem_UH => E_ReadMem_UH,
                ReadMem_SB => E_ReadMem_SB,
                ReadMem_UB => E_ReadMem_UB,
                WriteMem_W => E_WriteMem_W,
                WriteMem_H => E_WriteMem_H,
                WriteMem_B => E_WriteMem_B,
                WE => E_WE, 
                OE=> E_OE,
                clk => E_clk);

P_MEM_TEST: process
begin   
    E_address <= (others => '0');
    E_WriteMem_W <= '1';
    E_WriteMem_H <= '0';  
    E_WriteMem_B <= '0';
    E_ReadMem_W  <= '0';
    E_ReadMem_SH <= '0';
    E_ReadMem_UH <= '1';
    E_ReadMem_SB <= '0';
    E_ReadMem_UB <= '0';
    E_OE <= '0';
    E_data_in <= "11111111111010101010111111101110";    
    E_WE <= '0'; -- test ecriture ecriture
    E_clk <='0';
    wait for clkpulse;

    E_clk <='1';
    wait for clkpulse;

    E_WE <= '1'; -- test lecture
    E_clk <='0';
    wait for clkpulse;

    E_clk <='1';
    wait for clkpulse;

    E_clk <='0'; -- Test ecriture sur une autre addresse
    E_WE <= '0';
    E_address <= (0 => '1', others => '0');
    wait for clkpulse;

    E_clk <='1';
    wait for clkpulse;

    E_OE <= '1'; --test OE
    E_clk <='0';
    wait for clkpulse;

    E_clk <='1';
    wait for clkpulse;
    wait;

end process P_MEM_TEST;

end arch_memoire;