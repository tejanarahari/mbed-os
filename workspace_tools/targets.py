"""
mbed SDK
Copyright (c) 2011-2013 ARM Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

CORE_LABELS = {
    "ARM7TDMI-S": "ARM7",
    "Cortex-M0" : "M0",
    "Cortex-M0+": "M0P",
    "Cortex-M3" : "M3",
    "Cortex-M4" : "M4"
}

import os
import shutil


class Target:
    def __init__(self):
        # ARM Core
        self.core = None
        
        # Is the disk provided by the interface chip of this board virtual?
        self.is_disk_virtual = False
        
        # list of toolchains that are supported by the mbed SDK for this target
        self.supported_toolchains = None
        
        # list of extra specific labels
        self.extra_labels = []
        
        self.name = self.__class__.__name__
    
    def program_cycle_s(self):
        return 4 if self.is_disk_virtual else 1.5
    
    def get_labels(self):
        return [self.name, CORE_LABELS[self.core]] + self.extra_labels

    def init_hooks(self, hook, toolchain_name):
        pass


class LPC2368(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "ARM7TDMI-S"
        
        self.extra_labels = ['NXP', 'LPC23XX']
        
        self.supported_toolchains = ["ARM","GCC_ARM","GCC_CR"]


class LPC1768(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M3"
        
        self.extra_labels = ['NXP', 'LPC176X']
        
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM", "GCC_CS", "GCC_CR", "IAR"]


class LPC11U24(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0"
        
        self.extra_labels = ['NXP', 'LPC11UXX', 'LPC11U24_401']
        
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]


class LPC11U24_301(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0"
        
        self.extra_labels = ['NXP', 'LPC11UXX']
        
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]


class KL05Z(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0+"
        
        self.extra_labels = ['Freescale']
        
        self.supported_toolchains = ["ARM"]
        
        self.is_disk_virtual = True


class KL25Z(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0+"
        
        self.extra_labels = ['Freescale']
        
        self.supported_toolchains = ["ARM", "GCC_CW_EWL", "GCC_CW_NEWLIB", "GCC_ARM"]
        
        self.is_disk_virtual = True

class KL46Z(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0+"
        
        self.extra_labels = ['Freescale']

        self.supported_toolchains = ["GCC_ARM", "ARM"]

        self.is_disk_virtual = True


class LPC812(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0+"
        
        self.extra_labels = ['NXP', 'LPC81X']
        
        self.supported_toolchains = ["uARM"]
        
        self.is_disk_virtual = True


class LPC810(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0+"
        
        self.extra_labels = ['NXP', 'LPC81X']
        
        self.supported_toolchains = ["uARM"]
        
        self.is_disk_virtual = True


class LPC4088(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M4"
        
        self.extra_labels = ['NXP', 'LPC408X']
        
        self.supported_toolchains = ["ARM", "GCC_CR", "GCC_ARM"]
    
    def init_hooks(self, hook, toolchain_name):
        if toolchain_name in ['ARM_STD', 'ARM_MICRO']:
            hook.hook_add_binary("post", self.binary_hook)
    
    @staticmethod
    def binary_hook(t_self, resources, elf, binf):
        if not os.path.isdir(binf):
            # Regular binary file, nothing to do
            return
        outbin = open(binf + ".temp", "wb")
        partf = open(os.path.join(binf, "ER_IROM1"), "rb")
        # Pad the fist part (internal flash) with 0xFF to 512k
        data = partf.read()
        outbin.write(data)
        outbin.write('\xFF' * (512*1024 - len(data)))
        partf.close()
        # Read and append the second part (external flash) in chunks of fixed size
        chunksize = 128 * 1024
        partf = open(os.path.join(binf, "ER_IROM2"), "rb")
        while True:
            data = partf.read(chunksize)
            outbin.write(data)
            if len(data) < chunksize:
                break
        partf.close()
        outbin.close()
        # Remove the directory with the binary parts and rename the temporary
        # file to 'binf'
        shutil.rmtree(binf, True)
        os.rename(binf + '.temp', binf)
        t_self.debug("Generated custom binary file (internal flash + SPIFI)")


class LPC4330_M4(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M4"
        
        self.extra_labels = ['NXP', 'LPC43XX']
        
        self.supported_toolchains = ["ARM", "GCC_CR", "IAR", "GCC_ARM"]


class LPC4330_M0(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0"
        
        self.extra_labels = ['NXP', 'LPC43XX']
        
        self.supported_toolchains = ["ARM", "GCC_CR", "IAR"]


class LPC1800(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M3"
        
        self.extra_labels = ['NXP', 'LPC43XX']
        
        self.supported_toolchains = ["ARM", "GCC_CR", "IAR"]


class STM32F407(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M4"
        
        self.extra_labels = ['STM', 'STM32F4XX']
        
        self.supported_toolchains = ["ARM", "GCC_ARM"]


class MBED_MCU(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0+"
        
        self.extra_labels = ['ARM']
        
        self.supported_toolchains = ["ARM"]


class LPC1347(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M3"
        
        self.extra_labels = ['NXP', 'LPC13XX']
        
        self.supported_toolchains = ["ARM", "GCC_ARM"]


class LPC1114(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0"
        
        self.extra_labels = ['NXP', 'LPC11XX_11CXX', 'LPC11XX']
        
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]


class LPC11C24(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0"
        
        self.extra_labels = ['NXP', 'LPC11XX_11CXX', 'LPC11CXX']
        
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]


class LPC11U35_401(Target):
    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0"
        
        self.extra_labels = ['NXP', 'LPC11UXX']
        
        self.supported_toolchains = ["ARM", "uARM", "GCC_ARM"]


class nRF51822(Target):

    EXPECTED_SOFTDEVICE = 's110_nrf51822_6.0.0_softdevice.hex'
    UICR_START = 0x10001000
    APPCODE_OFFSET = 0x14000

    def __init__(self):
        Target.__init__(self)
        
        self.core = "Cortex-M0"
        
        self.extra_labels = ["NORDIC"]
        
        self.supported_toolchains = ["ARM"]

    def init_hooks(self, hook, toolchain_name):
        if toolchain_name in ['ARM_STD', 'ARM_MICRO']:
            hook.hook_add_binary("post", self.binary_hook)

    @staticmethod
    def binary_hook(t_self, resources, elf, binf):
        for hexf in resources.hex_files:
            if hexf.find(nRF51822.EXPECTED_SOFTDEVICE) != -1:
                break
        else:
            return
        # Generate hex file
        # NOTE: this is temporary, it will be removed later and only the
        # combined binary file (below) will be used
        from intelhex import IntelHex
        binh = IntelHex()
        binh.loadbin(binf, offset = nRF51822.APPCODE_OFFSET)
        sdh = IntelHex(hexf)
        sdh.merge(binh)
        outname = binf.replace(".bin", ".hex")
        with open(outname, "w") as f:
            sdh.tofile(f, format = 'hex')
        t_self.debug("Generated SoftDevice-enabled image in '%s'" % outname)
        # Generate concatenated SoftDevice + application binary
        # Currently, this is only supported for SoftDevice images that have
        # an UICR area
        sdh = IntelHex(hexf)
        if sdh.maxaddr() < nRF51822.UICR_START:
            t_self.error("SoftDevice image does not have UICR area, aborting")
            return
        addrlist = sdh.addresses()
        try:
            uicr_start_index = addrlist.index(nRF51822.UICR_START)
        except ValueError:
            t_self.error("UICR start address not found in the SoftDevice image, aborting")
            return
        # Assume that everything up to uicr_start_index are contiguous addresses
        # in the SoftDevice code area
        softdevice_code_size = addrlist[uicr_start_index - 1] + 1
        t_self.debug("SoftDevice code size is %d bytes" % softdevice_code_size)
        # First part: SoftDevice code
        bindata = sdh[:softdevice_code_size].tobinstr()
        # Second part: pad with 0xFF up to APPCODE_OFFSET
        bindata = bindata + '\xFF' * (nRF51822.APPCODE_OFFSET - softdevice_code_size)
        # Last part: the application code
        with open(binf, 'r+b') as f:
            bindata = bindata + f.read()
            # Write back the binary
            f.seek(0)
            f.write(bindata)
        t_self.debug("Generated concatenated binary of %d bytes" % len(bindata))

# Get a single instance for each target
TARGETS = [
    LPC2368(),
    LPC1768(),
    LPC11U24(),
    LPC11U24_301(),
    KL05Z(),
    KL25Z(),
    KL46Z(),
    LPC812(),
    LPC810(),
    LPC4088(),
    LPC4330_M4(),
    STM32F407(),
    MBED_MCU(),
    LPC1347(),
    LPC1114(),
    LPC11C24(),
    LPC11U35_401(),
    nRF51822()
]

# Map each target name to its unique instance
TARGET_MAP = {}
for t in TARGETS:
    TARGET_MAP[t.name] = t

TARGET_NAMES = TARGET_MAP.keys()

# Some targets with different name have the same exporters
EXPORT_MAP = {}
