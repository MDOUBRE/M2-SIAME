LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity Decodeur is
    port(
      entree :                                                          in std_logic_vector(5 downto 0);
      MemToReg, RegDst, UAL_Src, Jump :                                 out std_logic_vector(1 downto 0);
      UAL_Op :                                                          out std_logic_vector(1 downto 0);
      OpEXt, WR_Reg :                                                   out std_logic;
      B_eq, B_ne, B_lez, B_gtz, B_bltz, B_gezn, B_gez_AI, B_ltz_AI :    out std_logic;
      EcrireMem_W, EcrireMem_H, EcrireMem_B :                           out std_logic;
      LireMem_W, LireMem_SH, LireMem_UH, LireMem_SB, LireMem_UB :       out std_logic
      );
end entity;

architecture arch_Decodeur of Decodeur is
    signal m : std_logic_vector(63 downto 0);
begin
    m(0) <= '1' WHEN entree(5 downto 0) = "000000" else '0';
    m(1) <= '1' WHEN entree(5 downto 0) = "000001" else '0';
    m(2) <= '1' WHEN entree(5 downto 0) = "000010" else '0';
    m(3) <= '1' WHEN entree(5 downto 0) = "000011" else '0';
    m(4) <= '1' WHEN entree(5 downto 0) = "000100" else '0';
    m(5) <= '1' WHEN entree(5 downto 0) = "000101" else '0';
    m(6) <= '1' WHEN entree(5 downto 0) = "000110" else '0';
    m(7) <= '1' WHEN entree(5 downto 0) = "000111" else '0';
    m(8) <= '1' WHEN entree(5 downto 0) = "001000" else '0';
    m(9) <= '1' WHEN entree(5 downto 0) = "001001" else '0';
    m(10) <= '1' WHEN entree(5 downto 0) = "001010" else '0';
    m(11) <= '1' WHEN entree(5 downto 0) = "001011" else '0';
    m(12) <= '1' WHEN entree(5 downto 0) = "001100" else '0';
    m(13) <= '1' WHEN entree(5 downto 0) = "001101" else '0';
    m(14) <= '1' WHEN entree(5 downto 0) = "001110" else '0';
    m(15) <= '1' WHEN entree(5 downto 0) = "001111" else '0';
    m(16) <= '1' WHEN entree(5 downto 0) = "010000" else '0';
    m(17) <= '1' WHEN entree(5 downto 0) = "010001" else '0';
    m(18) <= '1' WHEN entree(5 downto 0) = "010010" else '0';
    m(19) <= '1' WHEN entree(5 downto 0) = "010011" else '0';
    m(20) <= '1' WHEN entree(5 downto 0) = "010100" else '0';
    m(21) <= '1' WHEN entree(5 downto 0) = "010101" else '0';
    m(22) <= '1' WHEN entree(5 downto 0) = "010110" else '0';
    m(23) <= '1' WHEN entree(5 downto 0) = "010111" else '0';
    m(24) <= '1' WHEN entree(5 downto 0) = "011000" else '0';
    m(25) <= '1' WHEN entree(5 downto 0) = "011001" else '0';
    m(26) <= '1' WHEN entree(5 downto 0) = "011010" else '0';
    m(27) <= '1' WHEN entree(5 downto 0) = "011011" else '0';
    m(28) <= '1' WHEN entree(5 downto 0) = "011100" else '0';
    m(29) <= '1' WHEN entree(5 downto 0) = "011101" else '0';
    m(30) <= '1' WHEN entree(5 downto 0) = "011110" else '0';
    m(31) <= '1' WHEN entree(5 downto 0) = "011111" else '0';
    m(32) <= '1' WHEN entree(5 downto 0) = "100000" else '0';
    m(33) <= '1' WHEN entree(5 downto 0) = "100001" else '0';
    m(34) <= '1' WHEN entree(5 downto 0) = "100010" else '0';
    m(35) <= '1' WHEN entree(5 downto 0) = "100011" else '0';
    m(36) <= '1' WHEN entree(5 downto 0) = "100100" else '0';
    m(37) <= '1' WHEN entree(5 downto 0) = "100101" else '0';
    m(38) <= '1' WHEN entree(5 downto 0) = "100110" else '0';
    m(39) <= '1' WHEN entree(5 downto 0) = "100111" else '0';
    m(40) <= '1' WHEN entree(5 downto 0) = "101000" else '0';
    m(41) <= '1' WHEN entree(5 downto 0) = "101001" else '0';
    m(42) <= '1' WHEN entree(5 downto 0) = "101010" else '0';
    m(43) <= '1' WHEN entree(5 downto 0) = "101011" else '0';

    MemToReg(0) <= m(32) or m(33) or m(35) or m(36) or m(37);
    MemToReg(1) <= m(0) or m(1) or m(3);

    OpExt <= m(1) or m(4) or m(5) or m(6) or m(7) or m(8) or m(10) or m(32) or m(33) or m(35) or m(36) or m(37) or m(40) or m(41) or m(43);

    RegDst(0) <= m(0);
    RegDst(1) <= m(1) or m(3);

    WR_Reg <= m(0) or m(1) or m(3) or m(8) or m(9) or m(10) or m(11) or m(12) or m(13) or m(14) or m(15) or m(32) or m(33) or m(35) or m(36) or m(37);

    UAL_Src(0) <= m(8) or m(9) or m(10) or m(11) or m(12) or m(13) or m(14) or m(15);
    UAL_Src(1) <= m(1) or m(15);

    UAL_Op(0) <= m(1) or m(4) or m(5) or m(6) or m(7) or m(8) or m(9) or m(10) or m(11) or m(12) or m(13) or m(14) or m(15);
    UAL_Op(1) <= m(0) or m(8) or m(9) or m(10) or m(11) or m(12) or m(13) or m(14) or m(15);

    B_eq <= m(4);
    B_ne <= m(5);
    B_lez <= m(6);
    B_gtz <= m(7);
    B_bltz <= m(1);
    B_gezn <= m(1);
    B_gez_AI <= m(1);
    B_ltz_AI <= m(1);

    EcrireMem_W <=  m(43);
    EcrireMem_H <= m(41);
    EcrireMem_B <= m(40);

    LireMem_W <= m(35);
    LireMem_SH <= m(33);
    LireMem_UH <= m(37);
    LireMem_SB <= m(32);
    LireMem_UB <= m(36);

    Jump(0) <= m(2) or m(3);
    Jump(1) <= m(0);

end arch_Decodeur;



LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity Ctrl_ALU is
    port(
      UAL_Op :              in std_logic_vector(1 downto 0);
      F, Op :               in std_logic_vector(5 downto 0);
      Sel :                 out std_logic_vector(3 downto 0);
      Slt_slti, Enable_V :  out std_logic
      );
end entity;

architecture arch_Ctrl_ALU of Ctrl_ALU is
begin

    Sel(0) <= '1' when (((UAL_Op(1) = '1' and UAL_Op(0) ='0') and 
          ((F(5)='0' and F(3 downto 0) = "0000") or (F(5)='1' and F(3 downto 0) = "1010")  or (F(5)='0' and F(3 downto 0) = "0110") or (F(5)='0' and F(3 downto 1) = "101"))) or
          ( UAL_Op(1) = '1' and UAL_Op(0) ='1' and (Op(1) = '1' or (Op(2) = '1' and Op(1) = '0' and Op(0) = '0') ) ))
          else '0';

    Sel(1) <= '1' when ( UAL_Op(1) = '0' or ( UAL_Op(1) = '1' and UAL_Op(0) = '0' and ( (F(3 downto 2) = "00" and F(0) = '0') or (F(5)='0' and F(3 downto 0) = "0100") or (F(5)='0' and F(3 downto 0) = "1001") or (F(5)='1' and F(3 downto 2) = "00" and F(0)='1') or (F(5)='0' and F(3 downto 0) = "101") ) )
          or ( UAL_Op(1 downto 0) = "11" and Op(2) = '0') ) 
          else '0' ;
          
    Sel(2) <= '1' when ( (UAL_Op(1 downto 0) = "10" and ( (F(5)='0' and F(3 downto 2) = "00" and F(0)='0') or (F(5)='0' and F(3 downto 1) = "011") ))
          or (UAL_Op(1 downto 0) = "11" and Op(2 downto 0) = "110") )
          else '0';

    Sel(3) <= '1' when  ( (UAL_Op(1 downto 0) = "01") or ( UAL_Op(1 downto 0) = "10" and ( (F(5)='1' and F(3 downto 1) = "001") or (F(5)='0' and F(3 downto 1) = "101") ) )
          or (UAL_Op(1 downto 0) = "11" and Op(2 downto 1) = "01") )
          else '0';

    Slt_slti <= '1' when  ( (UAL_Op(1 downto 0) = "10" and  F(3 downto 0) = "1010") or ( UAL_Op(1 downto 0) = "11" and Op(2 downto 0) = "010" ) )
          else '0';

    Enable_V <= '1' when  ( (UAL_Op(1 downto 0) = "10" and F(5) = '1' and F(2) = '0' and F(0) = '0') or ( UAL_Op(1 downto 0) = "00" ) )
          else '0';

end arch_Ctrl_ALU;



LIBRARY IEEE;
USE IEEE.STD_LOGIC_1164.ALL;
USE IEEE.NUMERIC_STD.ALL;

entity Ctrl_PC is
    port(
      -- N, Z, B_eq, B_ne, B_lez, B_gtz, B_bltz, B_gez, B_gez_AI, B_itz_AI, rt0 : in std_logic;
      N, Z, m4, m5, m6, m7, m1, rt0, rt4 : in std_logic;
      CPSrc : out std_logic
      );
end entity;
  
architecture arch_Ctrl_PC of Ctrl_PC is
begin
    --CPSrc <= '1' when ( (B_eq = '1' and Z = '1') or (B_ne = '1' and Z = '0') or (B_lez = '1' and (N = '1' or Z = '1')) or (B_gtz = '1' and N = '0' and Z = '0')
    --            or (B_bltz = '1' and N = '1' and Z = '0') or (B_gez = '1' and (N = '0' or Z = '1')) or ( B_itz_AI = '1' and rt0 = '0' and N = '1' and Z = '0') or ( B_gez_AI = '1' and rt0 = '1' and (N = '0' or Z = '1') )  ) 
    --            else '0';       
    
    CpSrc <= (m4 and Z) or (m5 and not(Z)) or (m6 and (N or Z)) or (m7 and not(Z) and not(N)) or (m1 and ( (N and not(Z) and not(rt0)) or ((not(N) or Z) and rt0 )));
end arch_Ctrl_PC;