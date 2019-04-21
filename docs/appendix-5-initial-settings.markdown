# Appendix 5. Initial Settings

The various switches and useful variables in MDL are initially set up with the following values:

    <ACTIVAIE-CHARS <STRING <ASCII 7> <ASCII 19> <ASCII 15>>>
                          ;"Tenex and Tops-20 versions only"
    <DECL-CHECK T>
    <UNASSIGN <GUNASSIGN DEV>>
    <GC-MON <>>
    <SET INCHAN <SETG INCHAN <OPEN "READ" "TTY:">>>
    <UNASSIGN KEEP-FIXUPS>
    <UNASSIGN <GUNASSIGN NM1>>
    <UNASSIGN <GUNASSIGN NM2>>
    <SET OBLIST <SETG OBLIST (<MOBLIST INITIAL 151> <ROOT>)>>
    <SET OUTCHAN <SETG OUTCHAN <OPEN "PRINT" "TTY:">>>
    <OVERFLOW T>
    <UNASSIGN REDEFINE>
    <RSUBR-LINK T>
    <SETG <UNASSIGN SNM> "working-directory">
    <SPECIAL-CHECK <>>
    <SPECIAL-MODE UNSPECIAL>
    <SET THIS-PROCESS <SETG THIS-PROCESS <MAIN>>>
    <ON "CHAR" .QUITTER 8 0 ,INCHAN>
    <ON "IPC" ,IPC-HANDLER 1>               ;"ITS version only"
