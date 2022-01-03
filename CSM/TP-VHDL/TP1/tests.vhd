LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_Reg is
end test_Reg;

architecture arch_test_Reg of test_Reg is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

signal E_source     : std_logic_vector(31 downto 0);
signal E_output     : std_logic_vector(31 downto 0);
signal E_wr         : std_logic;
signal E_clk        : std_logic;

begin 

regf0 : entity work.Reg
    port map (clk => E_clk,
                source => E_source,
                output => E_output,
                wr => E_wr);

P_TEST: process
begin
    E_clk<='0';  
    E_wr<='0';
    E_source <= (0=>'1', others => '0');
    wait for clkpulse;

    E_clk<='1'; 
    E_wr <='1';
    wait for clkpulse;

    E_clk<='0';
    E_wr<='0';
    E_source <= (0=>'1', 2=>'1', others => '0');
    wait for clkpulse;

    E_clk<='1'; 
    E_wr <='0';
    wait for clkpulse;   
    
    E_clk<='0'; 
    E_wr <='1';
    wait for clkpulse;   

    E_clk<='1'; 
    E_wr <='1';
    wait for clkpulse;   

    wait;

end process P_TEST;

end arch_test_Reg;


LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_Banc_Reg is
end test_Banc_Reg;

architecture arch_test_Banc_Reg of test_Banc_Reg is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

signal E_s_reg_0   :   std_logic_vector(4 DOWNTO 0) := ("00000");
signal E_data_o_0  :   std_logic_vector(31 DOWNTO 0);
signal E_s_reg_1   :   std_logic_vector(4 DOWNTO 0) := ("00000");
signal E_data_o_1  :   std_logic_vector(31 DOWNTO 0);
signal E_dest_reg  :   std_logic_vector(4 DOWNTO 0);
signal E_data_i    :   std_logic_vector(31 DOWNTO 0);
signal E_wr_reg    :   std_logic;
signal E_clk       :   std_logic;

begin 

regf0 : entity work.RegisterBank
    port map (clk => E_clk,
                s_reg_0 => E_s_reg_0,
                data_o_0 => E_data_o_0,
                s_reg_1 => E_s_reg_1,
                data_o_1 => E_data_o_1,
                dest_reg => E_dest_reg, 
                data_i => E_data_i,
                wr_reg => E_wr_reg);

P_BANC_TEST: process
begin
    E_clk <='0';  
    E_wr_reg <='0';
    E_data_i <= (0 => '1', 2 => '1', others => '0');
    wait for clkpulse;

    E_clk <='1'; 
    E_wr_reg <='1';
    E_dest_reg <= (2 => '1', others => '0');
    wait for clkpulse;

    E_clk <='0';
    E_wr_reg <='0';
    E_s_reg_0 <= (2 => '1', others => '0');
    wait for clkpulse;

    E_clk<='1'; 
    E_wr_reg <='0';
    E_s_reg_1 <= (2 => '1', others => '0');
    wait for clkpulse;     

    wait;

end process P_BANC_TEST;
    
end arch_test_Banc_Reg;

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



LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity test_ALU is
end test_ALU;

architecture arch_test_alu of test_ALU is

constant clkpulse : Time := 10 ns; -- 1/2 periode horloge

signal E_A : std_logic_vector(31 downto 0); 
signal E_B : std_logic_vector(31 downto 0); 
signal E_sel : std_logic_vector(3 downto 0); 
signal E_Enable_V : std_logic;
signal E_ValDec : std_logic_vector(4 DOWNTO 0);
signal E_Slt : std_logic;
signal E_CLK : std_logic;
signal E_Res : std_logic_vector(31 DOWNTO 0);
signal E_N : std_logic;
signal E_Z : std_logic;
signal E_C : std_logic;
signal E_V : std_logic;

begin 

regf0 : entity work.ALU
    port map (A => E_A,
                B => E_B, 
                sel => E_sel, 
                Enable_V => E_Enable_V, 
                ValDec => E_ValDec,
                Slt => E_Slt, 
                CLK => E_CLK,
                Res => E_Res, 
                N => E_N, 
                Z => E_Z,
                C => E_C, 
                V => E_V);    

P_ALU_TEST: process
begin
    E_CLK <= '1';
    E_A <= (0 => '1', 1 => '1', 3 => '1', others => '0');
    E_B <= (1 => '1', 3 => '1', 4 => '1', 5 => '1', others => '0');
    E_sel <= "0000";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    E_CLK <= '1';
    E_sel <= "0001";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    E_CLK <= '1';
    E_sel <= "0010";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    E_CLK <= '1';
    E_sel <= "0011";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    E_CLK <= '1';
    E_sel <= "0100";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    E_CLK <= '1';
    E_sel <= "0101";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    E_CLK <= '1';
    E_sel <= "0110";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    E_CLK <= '1';
    E_sel <= "0111";
    wait for clkpulse;

    E_CLK <= '0';
    wait for clkpulse;

    wait;

end process P_ALU_TEST;
end arch_test_alu;