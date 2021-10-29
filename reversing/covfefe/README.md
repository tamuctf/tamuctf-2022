# Covfefe

## Description

This one might require a nice hot cup of Java to get through.

## Solution
Apparently, Ghidra supports .class files, so I took the decompiled output, cleaned it up a bit, then printed the buffer that it modified. 
```c
#include <stdlib.h>
#include <stdio.h>

int main(void) {
    double dVar1;
    int iVar2;
    char* piVar3 = calloc(0x24, 1);
    int iVar4;
    int iVar5;
    char* piVar6;
    int iVar7;
    char* piVar8;
    int iVar9;
    char* piVar10;
    int iVar11;
    char* piVar12;

    iVar2 = 0x23;
    piVar3[0] = 0x67;
    piVar3[1] = piVar3[0] + 2;
    piVar3[2] = piVar3[0];
    for (iVar4 = 3; iVar4 < 8; iVar4 = iVar4 + 1) {
        switch(iVar4) {
            case 3:
                piVar3[iVar4] = 0x65;
                break;
            case 4:
                piVar3[6] = 99;
                break;
            case 5:
                piVar3[5] = 0x7b;
                break;
            case 6:
                piVar3[iVar4 + 1] = 0x30;
                break;
            case 7:
                piVar3[4] = 0x6d;
        }
    }
    piVar3[8] = 0x66;
    piVar3[9] = piVar3[8];
    iVar4 = piVar3[7];
    piVar3[0x1c] = iVar4;
    piVar3[0x19] = iVar4;
    piVar3[0x18] = iVar4;
    piVar3[10] = 0x33;
    piVar3[0xb] = piVar3[10];
    iVar11 = 0xc;
    iVar9 = 0xf;
    iVar7 = 0x16;
    iVar5 = 0x1b;
    iVar4 = piVar3[0];
    piVar6 = piVar3;
    piVar12 = piVar3;
    piVar8 = piVar3;
    piVar10 = piVar3;
    // Math.pow(2.0,3.0)
    dVar1 = 8;
    iVar4 = iVar4 - dVar1;
    piVar6[iVar5] = iVar4;
    piVar8[iVar7] = iVar4;
    piVar10[iVar9] = iVar4;
    piVar12[iVar11] = iVar4;
    piVar3[0xd] = 0x31;
    piVar3[0xe] = 0x73;
    for (iVar4 = 0x10; iVar4 < 0x16; iVar4 = iVar4 + 1) {
        switch(iVar4) {
            case 0x10:
                piVar3[iVar4 + 1] = 0x6c;
                break;
            case 0x11:
                piVar3[iVar4 + -1] = 0x34;
                break;
            case 0x12:
                piVar3[iVar4 + 1] = 0x34;
                break;
            case 0x13:
                piVar3[iVar4 + -1] = 0x77;
                break;
            case 0x14:
                piVar3[iVar4 + 1] = 0x73;
                break;
            case 0x15:
                piVar3[iVar4 + -1] = 0x79;
        }
    }
    piVar3[0x17] = 0x67;
    piVar3[0x1a] = piVar3[0x17] + -3;
    piVar3[0x1d] = piVar3[0x1a] + 0x14;
    piVar3[0x1e] = piVar3[0x1d] % 0x35 + 0x35;
    piVar3[0x1f] = piVar3[0] + -0x12;
    piVar3[0x20] = 0x50;
    piVar3[0x21] = 0x53;
    iVar2 = iVar2 + -1;
    // Math.pow(5.0,3.0)
    dVar1 = 125;
    // piVar3[iVar2] = SUB84(ROUND(dVar1),0);
    piVar3[iVar2] = dVar1;
    piVar3[0x24 - 1] = 0;
    puts(piVar3);
    return 0;
}
```
Flag: gigem{c0ff33_1s_4lw4ys_g00d_0xCUPS}
