LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_Mux is
end test_Mux;

architecture arch_test_Mux of test_Mux is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge
constant size : Integer := 6;

signal E_reg0     : std_logic_vector(size-1 downto 0);
signal E_reg1     : std_logic_vector(size-1 downto 0);
signal E_reg2     : std_logic_vector(size-1 downto 0);
signal E_reg3     : std_logic_vector(size-1 downto 0);
signal E_reg_out  : std_logic_vector(size-1 downto 0);
signal E_c        : std_logic_vector(1 downto 0);

begin 

regf0 : entity work.mux4_1
    generic map(size)
    port map (reg0 => E_reg0,
                reg1 => E_reg1,
                reg2 => E_reg2, 
                reg3 => E_reg3, 
                reg_out => E_reg_out, 
                c => E_c);

P_MUX_TEST: process
begin
    E_reg0 <= "000001";
    E_reg1 <= "000010";
    E_reg2 <= "000100";
    E_reg3 <= "001000";
    E_c <= "10";
    wait for clkpulse;

    E_reg0 <= "000001";
    E_reg1 <= "000010";
    E_reg2 <= "000100";
    E_reg3 <= "001000";
    E_c <= "00";
    wait for clkpulse;

    E_c <= "01";
    wait for clkpulse;

    E_reg0 <= "000001";
    E_reg1 <= "000010";
    E_reg2 <= "000100";
    E_reg3 <= "001000";
    E_c <= "11";
    wait for clkpulse;    

    wait;

end process P_MUX_TEST;

end arch_test_Mux;



LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_Add is
end test_Add;

architecture arch_test_Add of test_Add is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

signal E_reg1 : std_logic_vector(31 downto 0); 
signal E_reg2 : std_logic_vector(31 downto 0);
signal E_reg3 : std_logic_vector(31 downto 0);

begin 

regf0 : entity work.add
    port map (reg1 => E_reg1,
                reg2 => E_reg2, 
                reg3 => E_reg3);

P_ADD_TEST: process
begin
    E_reg1 <= (0 => '1', others => '0');
    E_reg2 <= (1 => '1', others => '0');
    wait for clkpulse;

    E_reg1 <= (2 => '1', others => '0');
    E_reg2 <= (0 => '1', others => '0');
    wait for clkpulse;

    wait;

end process P_ADD_TEST;

end arch_test_Add;



LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_AddCarry is
end test_AddCarry;

architecture arch_test_AddCarry of test_AddCarry is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

signal E_A : std_logic_vector(31 downto 0); 
signal E_B : std_logic_vector(31 downto 0); 
signal E_s : std_logic_vector(31 downto 0); 
signal E_cin : std_logic;
signal E_c30 : std_logic;
signal E_c31 : std_logic;

begin 

regf0 : entity work.addCarry
    port map (A => E_A,
                B => E_B, 
                s => E_s, 
                cin => E_cin, 
                c30 => E_c30, 
                c31 => E_c31);    

P_ADD_TEST: process
begin
    E_A <= (0 => '1', 1 => '1', others => '0');
    E_B <= (1 => '1', others => '0');
    E_cin <= '0';
    wait for clkpulse;

    E_A <= (others => '1');
    E_B <= (others => '1');
    wait for clkpulse;

    wait;

end process P_ADD_TEST;
end arch_test_AddCarry;



LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_BArrelShifter is
end test_BArrelShifter;

architecture arch_test_BarrelShifter of test_BarrelShifter is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

signal E_A : std_logic_vector(31 downto 0);
signal E_ValDec : std_logic_vector(4 downto 0);
signal E_SR : std_logic_vector(31 downto 0); 
signal E_SL : std_logic_vector(31 downto 0); 

begin 

regf0 : entity work.BarrelShifter
    port map (A => E_A,
                ValDec => E_ValDec, 
                SR => E_SR, 
                SL => E_SL);    

P_ADD_TEST: process
begin
    E_A <= (3 => '1', 4 => '1', 5 => '1', others => '0');
    E_ValDec <= (others => '0');
    wait for clkpulse;
    
    E_A <= (3 => '1', 4 => '1', 5 => '1', others => '0');
    E_ValDec <= (0 => '1', others => '0');
    wait for clkpulse;

    E_A <= (3 => '1', 4 => '1', 5 => '1', others => '0');
    E_ValDec <= (1 => '1', others => '0');
    wait for clkpulse;
    
    E_A <= (3 => '1', 4 => '1', 5 => '1', others => '0');
    E_ValDec <= (2 => '1', others => '0');
    wait for clkpulse;

    E_A <= (3 => '1', 4 => '1', 5 => '1', others => '0');
    E_ValDec <= (3 => '1', others => '0');
    wait for clkpulse;

    E_A <= (3 => '1', 4 => '1', 5 => '1', others => '0');
    E_ValDec <= (4 => '1', others => '0');
    wait for clkpulse;

    wait;

end process P_ADD_TEST;

end arch_test_BarrelShifter;

