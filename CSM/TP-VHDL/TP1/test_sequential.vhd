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
