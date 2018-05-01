################################################################################
# Automatically-generated file. Do not edit!
################################################################################

SHELL = cmd.exe

# Each subdirectory must supply rules for building sources it contributes
fft.obj: ../fft.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: C5500 Compiler'
	"C:/ti/ccsv7/tools/compiler/c5500_4.4.1/bin/cl55" -v5502 -g --include_path="C:/ti/ccsv7/tools/compiler/c5500_4.4.1/include" --include_path="C:/Program Files (x86)/Texas Instruments/ccsv4/emulation/boards/ezdsp5502_v1/C55xxCSL/include" --include_path="C:/Program Files (x86)/Texas Instruments/ccsv4/emulation/boards/ezdsp5502_v1/include" --diag_warning=225 --ptrdiff_size=32 --memory_model=large --preproc_with_compile --preproc_dependency="fft.d" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

main.obj: ../main.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: C5500 Compiler'
	"C:/ti/ccsv7/tools/compiler/c5500_4.4.1/bin/cl55" -v5502 -g --include_path="C:/ti/ccsv7/tools/compiler/c5500_4.4.1/include" --include_path="C:/Program Files (x86)/Texas Instruments/ccsv4/emulation/boards/ezdsp5502_v1/C55xxCSL/include" --include_path="C:/Program Files (x86)/Texas Instruments/ccsv4/emulation/boards/ezdsp5502_v1/include" --diag_warning=225 --ptrdiff_size=32 --memory_model=large --preproc_with_compile --preproc_dependency="main.d" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '

sdram_test.obj: ../sdram_test.c $(GEN_OPTS) | $(GEN_HDRS)
	@echo 'Building file: $<'
	@echo 'Invoking: C5500 Compiler'
	"C:/ti/ccsv7/tools/compiler/c5500_4.4.1/bin/cl55" -v5502 -g --include_path="C:/ti/ccsv7/tools/compiler/c5500_4.4.1/include" --include_path="C:/Program Files (x86)/Texas Instruments/ccsv4/emulation/boards/ezdsp5502_v1/C55xxCSL/include" --include_path="C:/Program Files (x86)/Texas Instruments/ccsv4/emulation/boards/ezdsp5502_v1/include" --diag_warning=225 --ptrdiff_size=32 --memory_model=large --preproc_with_compile --preproc_dependency="sdram_test.d" $(GEN_OPTS__FLAG) "$<"
	@echo 'Finished building: $<'
	@echo ' '


