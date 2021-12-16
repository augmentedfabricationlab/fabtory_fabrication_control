MODULE Main_Module

    CONST jointtarget pj_StartPosition:=[[0,-34,60,0,60,0],[2000,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST jointtarget pj_ausgestreckt:=[[-99.3287,57.2425,-48.8396,0.000296201,13.9978,-5.75035E-05],[4091.17,9E+09,9E+09,9E+09,9E+09,9E+09]];

    CONST robtarget pSofwareende_X_Minus:=[[687.15,-818.98,994.32],[0.00754222,-0.422758,-0.906205,-0.00349207],[-1,0,0,0],[0.00153582,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pSofwareende_X_Plus:=[[3653.65,-758.18,869.72],[0.02198,-0.905164,-0.421875,-0.0470823],[-2,0,0,0],[4290,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget pX_MittelstellungAusgestreckt:=[[2147.72,-130.42,3850.79],[0.706837,0.0345686,0.0244452,-0.706108],[-1,-1,0,2],[2150,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST robtarget p_StartpunktQuadrat:=[[2149.85,-1738.60,178.78],[6.6479E-06,-0.707244,-0.70697,-7.69143E-06],[-1,-1,0,0],[2150,9E+09,9E+09,9E+09,9E+09,9E+09]];

    CONST speeddata v_schnell:=v7000;
    CONST speeddata v_250mm_s:=[250,500,250,0];

    CONST speeddata v_ReduziertEllebogen:=[200,100,150,0];
    CONST speeddata v_ReduziertEllebogen_2:=[100,50,100,0];


    PROC MainIBN()

        ! Beschleunigung und Verzögerung begrenzen (in m/s 2)
        PathAccLim TRUE\AccMax:=0.25,TRUE\DecelMax:=0.25;

        Bremsentest;

        AblaufAbnahme;

    ENDPROC

    PROC AblaufAbnahme()

        MoveAbsJ pj_StartPosition\NoEOffs,v_ReduziertEllebogen,fine,tool0\WObj:=wobj0;

        MoveJ pSofwareende_X_Plus,v_ReduziertEllebogen,z10,tool0\WObj:=wobj0;

        MoveAbsJ pj_ausgestreckt\NoEOffs,v_ReduziertEllebogen,fine,tool0;

        MoveJ Offs(p_StartpunktQuadrat,0,0,500),v_ReduziertEllebogen,z5,tool0\WObj:=wobj0;
        MoveL p_StartpunktQuadrat,v_ReduziertEllebogen_2,fine,tool0\WObj:=wobj0;
        MoveLDO Offs(p_StartpunktQuadrat,1000,0,0),v_250mm_s,fine,tool0\WObj:=wobj0,Ausgang_100_3,1;
        MoveLDO Offs(p_StartpunktQuadrat,1000,-1000,0),v_250mm_s,fine,tool0\WObj:=wobj0,Ausgang_100_3,0;

        MoveLDO Offs(p_StartpunktQuadrat,100,-1000,0),v_250mm_s,z1,tool0\WObj:=wobj0,Ausgang_100_3,1;
        MoveLDO Offs(p_StartpunktQuadrat,-100,-1000,0),v50,z1,tool0\WObj:=wobj0,Ausgang_100_3,0;
        MoveL Offs(p_StartpunktQuadrat,-1000,-1000,0),v_250mm_s,z5,tool0\WObj:=wobj0;

        MoveL Offs(p_StartpunktQuadrat,-1000,0,0),v_250mm_s,z5,tool0\WObj:=wobj0;
        MoveL p_StartpunktQuadrat,v_250mm_s,fine,tool0\WObj:=wobj0;

        MoveJ pSofwareende_X_Minus,v_ReduziertEllebogen_2,z10,tool0\WObj:=wobj0;

        MoveJ pX_MittelstellungAusgestreckt,v_schnell,z200,tool0\WObj:=wobj0;

        MoveAbsJ pj_StartPosition\NoEOffs,v_schnell,fine,tool0\WObj:=wobj0;

    ENDPROC


    PROC Bremsentest()

        ! Prüfe ob ein Bremsentest vom Roboter angefordert wird
        IF SC1CBCPREWARN=1 OR SC1CBCREQ=1 THEN

            MoveAbsJ pj_StartPosition\NoEOffs,v_ReduziertEllebogen,fine,tool0\WObj:=wobj0;

            cyclicbrakecheck;

            ! Wenn Bremsentest nicht i.O. war, anhalten
            IF SC1CBCOK=0 THEN
                TPErase;
                TPWrite "Bremsentest war n.i.O.";
                Stop;
            ENDIF

        ENDIF

    ENDPROC

ENDMODULE