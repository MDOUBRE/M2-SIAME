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