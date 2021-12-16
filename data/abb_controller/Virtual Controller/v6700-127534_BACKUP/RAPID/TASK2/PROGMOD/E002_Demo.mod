MODULE E002_Demo


    !***********************************************************************************
    !
    ! ETH Zurich / Robotic Fabrication Lab
    ! HIB C 13 / Stefano-Franscini-Platz 1
    ! CH-8093 Zurich
    !
    !***********************************************************************************
    !
    ! PROJECT     :  E002
    !
    ! FUNCTION    :  Demo
    !
    ! AUTHOR      :  Philippe Fleischmann
    !
    ! EMAIL       :  fleischmann@arch.ethz.ch
    !
    ! HISTORY     :  2021.11.26
    !
    ! Copyright   :  ETH Zurich (CH) 2020
    !                - Philippe Fleischmann
    !
    ! License     :  You agree that the software source code and documentation
    !                provided by the copyright holder is confidential,
    !                and you shall take all reasonable precautions to protect
    !                the source code and documentation, and preserve its confidential,
    !                proprietary and trade secret status in perpetuity.
    !
    !                This license is strictly limited to INTERNAL use within one site.
    !
    !***********************************************************************************

    !************************************************
    ! Declaration :     jointtarget
    !************************************************
    !
    TASK PERS jointtarget jp_E002_Pos1:=[[-116.973,47.2655,-4.81397,9.30512,-43.8047,-9.66109],[2383.85,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jp_E002_Pos2:=[[-116.973,76.6496,-18.2488,7.45689,-59.5878,-6.70802],[2383.85,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jp_E002_Pos3:=[[-116.973,70.5531,-13.9338,7.59887,-57.8212,-6.98115],[2383.85,9E+09,9E+09,9E+09,9E+09,9E+09]];
    TASK PERS jointtarget jp_E002_Pos4:=[[-96.2785,63.3623,2.22623,29.1479,-69.3653,-14.4227],[1470.09,9E+09,9E+09,9E+09,9E+09,9E+09]];

    !************************************************
    ! Declaration :     jointtarget
    !************************************************
    !
    TASK PERS speeddata v_E002_Demo:=[240,500,200,1];



    !************************************************
    ! Function    :     Go to software sychnronizeition position
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2021.11.26
    !***************** ETH Zürich *******************
    !
    PROC r_E002_Demeo_old()
        !
        WHILE TRUE DO

            MoveAbsJ jp_E002_Pos1\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;
            MoveAbsJ jp_E002_Pos2\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;
            MoveAbsJ jp_E002_Pos3\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;
            MoveAbsJ jp_E002_Pos4\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;


        ENDWHILE
        !
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC


    !************************************************
    ! Function    :     Custom Instruction
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.22
    !***************** ETH Zurich *******************
    !
    PROC r_E002_Demeo()
        !
        WHILE TRUE DO

            MoveAbsJ jp_E002_Pos1\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;
            MoveAbsJ jp_E002_Pos2\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;
            MoveAbsJ jp_E002_Pos3\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;
            MoveAbsJ jp_E002_Pos4\NoEOffs,v_E002_Demo,z1,tool0\WObj:=wobj0;

        ENDWHILE
        !
        ! Placehoder for your Code
        !
        ! Feedback
        IF bm_RRC_RecBufferRob{n_RRC_ChaNr,n_RRC_ReadPtrRecBuf}.Data.F_Lev>0 THEN
            !
            ! Cenerate feedback
            TEST bm_RRC_RecBufferRob{n_RRC_ChaNr,n_RRC_ReadPtrRecBuf}.Data.F_Lev
            CASE 1:
                !
                ! Instruction done 
                r_RRC_FDone;
            DEFAULT:
                !
                ! Feedback not supported  
                r_RRC_FError;
            ENDTEST
            !
            ! Move message in send buffer
            r_RRC_MovMsgToSenBufRob n_RRC_ChaNr;
        ENDIF
        RETURN ;
    ERROR
        ! Placeholder for Error Code...
    ENDPROC


ENDMODULE