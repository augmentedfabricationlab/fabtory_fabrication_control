MODULE E002_DataTask


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
    ! FUNCTION    :  Task Data
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
    TASK PERS tooldata t_E002_Tool_X:=[TRUE,[[225,0,40],[0.707106781,0,0.707106781,0]],[0,[0,0,0],[1,0,0,0],0,0,0]];

    !************************************************
    ! Declaration :     jointtarget
    !************************************************
    !
    TASK PERS wobjdata ob_E002_Table_X:=[FALSE,TRUE,"",[[1786.5,-2464,-400],[1,0,0,0]],[[0,0,0],[1,0,0,0]]];

ENDMODULE