MODULE IBN

    CONST jointtarget pj_Kalibrierposition:=[[0,0,0,0,0,0],[2000,9E+09,9E+09,9E+09,9E+09,9E+09]];

    
    PROC FahreInKalibrierpostition()
        MoveAbsJ pj_Kalibrierposition\NoEOffs,v100,fine,tool0;
    ENDPROC

    PROC IBN_SyncPos()
        MoveJ pSofwareende_X_Minus,v_schnell,fine,tool0\WObj:=wobj0;
    ENDPROC

ENDMODULE