MODULE Main_Module

    CONST jointtarget pj_10:=[[-50,-33.9995,70.0008,0.000204008,59.9998,0.00015541],[0,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST jointtarget pj_ausgestreckt:=[[-90,85,-85,0,0,0],[4290,9E+09,9E+09,9E+09,9E+09,9E+09]];

    CONST robtarget pSofwareende_X_Minus:=[[687.15,-818.98,994.32],[0.00754222,-0.422758,-0.906205,-0.00349207],[-1,0,0,0],[0.00153582,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pSofwareende_X_Plus:=[[3653.65,-758.18,869.72],[0.02198,-0.905164,-0.421875,-0.0470823],[-2,0,0,0],[4290,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget p10:=[[-749.47,-3008.95,869.75],[4.92695E-08,-0.422792,-0.906227,1.48874E-06],[-2,-1,-1,0],[0.000254038,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pX_Mittelstellung:=[[2149.85,-989.74,869.74],[0.0367541,-0.706286,-0.706018,-0.0367162],[-2,0,0,0],[2150,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pX_MittelstellungAusgestreckt:=[[1845.87,-1478.56,3469.22],[0.445936,0.492885,0.541057,-0.515231],[-2,0,-1,0],[1883.57,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget p_Startpunkt1x1m:=[[2149.85,-1738.60,178.78],[6.6479E-06,-0.707244,-0.70697,-7.69143E-06],[-1,-1,0,0],[2150,9E+09,9E+09,9E+09,9E+09,9E+09]];
    
    
    CONST robtarget Testmf:=[[0,0,0],[1,0,0,0],[0,0,0,0],[9E9,9E9,9E9,9E9,9E9,9E9]];


    CONST speeddata v_schnell:=[250,250,250,0];
   
    CONST speeddata v_langsam:=[100,10,50,0];

    PROC Main()
        AblaufAbnahme;
    ENDPROC

    PROC AblaufAbnahme()

        ! MoveJ pSofwareende_X_Minus,v_schnell,z10,tool0\WObj:=wobj0;  

        MoveJ pSofwareende_X_Plus,v_schnell,z10,tool0\WObj:=wobj0;

    

        MoveJ pX_MittelstellungAusgestreckt,v_schnell,z200,tool0\WObj:=wobj0;
         MoveJ Offs(p_Startpunkt1x1m,0,0,500),v_schnell,z5,tool0\WObj:=wobj0;
         MoveAbsJ pj_Position_ausgepackt\NoEOffs,v_schnell,fine,tool0\WObj:=wobj0;
        
!        MoveJ p10,v_schnell,z10,tool0\WObj:=wobj0;
!        MoveL Offs(p10,0,0,-100),v_langsam,fine,tool0\WObj:=wobj0;
!        WaitTime 1;
!        MoveL p10,v_langsam,z10,tool0\WObj:=wobj0;

!        MoveJ Offs(p_Startpunkt1x1m,0,0,500),v_schnell,z5,tool0\WObj:=wobj0;
!        MoveL p_Startpunkt1x1m,v_schnell,fine,tool0\WObj:=wobj0;
!        Set Ausgang_100_2;
!        WaitTime 1;
!        Reset Ausgang_100_2;
!        MoveL Offs(p_Startpunkt1x1m,500,0,0),v_schnell,z5,tool0\WObj:=wobj0;
!        MoveL Offs(p_Startpunkt1x1m,500,-500,0),v_schnell,z5,tool0\WObj:=wobj0;
!        MoveL Offs(p_Startpunkt1x1m,-500,-500,0),v_schnell,z5,tool0\WObj:=wobj0;
!        MoveL Offs(p_Startpunkt1x1m,-500,0,0),v_schnell,z5,tool0\WObj:=wobj0;
!        MoveL Offs(p_Startpunkt1x1m,0,0,500),v_schnell,z5,tool0\WObj:=wobj0;

!        MoveAbsJ pj_Position_ausgepackt\NoEOffs,v_schnell,fine,tool0\WObj:=wobj0;

    ENDPROC

ENDMODULE