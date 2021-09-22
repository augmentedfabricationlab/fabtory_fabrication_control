MODULE IBN

    CONST jointtarget pj_Position_ausgepackt:=[[0,-34,70,0,60,0],[2000,9E+09,9E+09,9E+09,9E+09,9E+09]];
    CONST jointtarget pj_Kalibrierposition:=[[0,0,0,0,0,0],[2000,9E+09,9E+09,9E+09,9E+09,9E+09]];
   
    ! Achsewerte Position augepackt:
    ! 1:    0.00
    ! 2: -34.00
    ! 3:  70.06
    ! 4:   0.00
    ! 5:  60.15
    ! 6:   0.00

    PROC FahreInKalibrierpostition()
        MoveAbsJ pj_Kalibrierposition\NoEOffs,v100,fine,tool0;
    ENDPROC

    PROC FahreInAuspackposition()
        MoveAbsJ pj_Position_ausgepackt\NoEOffs,v100,fine,tool0;
    ENDPROC
  
    PROC IBN_SyncPos()
        MoveJ pSofwareende_X_Minus,v_schnell,fine,tool0\WObj:=wobj0;
    ENDPROC

    PROC Ibn_ausgestreckt()
        MoveAbsJ pj_ausgestreckt\NoEOffs,v1000,fine,tool0;
    ENDPROC

ENDMODULE