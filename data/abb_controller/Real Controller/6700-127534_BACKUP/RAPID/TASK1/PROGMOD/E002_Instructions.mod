MODULE E002_Instructions
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
    ! FUNCTION    :  All user instructions 
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
    ! Function    :     Custom Instruction
    ! Programmer  :     Philippe Fleischmann
    ! Date        :     2019.02.22
    !***************** ETH Zurich *******************
    !
    PROC r_E002_Gripper_On()
        !
        ! Read string value
        st_RRC_StringValue:=bm_RRC_RecBufferRob{n_RRC_ChaNr,n_RRC_ReadPtrRecBuf}.Data.St1;
        !
        ! Read float value
        n_RRC_FloatValue:=bm_RRC_RecBufferRob{n_RRC_ChaNr,n_RRC_ReadPtrRecBuf}.Data.V1;
        !
        ! Open dummy gripper
        SetDO Ausgang_100_0,1;
        !
        ! User message
        TPWrite st_RRC_StringValue\Num:=n_RRC_FloatValue;
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