"""
Generated command-line help specification for llama-server.
Generated on 2026-08-26T12:07:22.648985
"""

from __future__ import annotations

from typing import Any

HELP_SPEC: dict[str, Any] = {   'program': 'llama-server',
    'usage': 'llama-server [options]',
    'sections': {   'options': [],
                    'common params': [   {   'aliases': ['-h', '--help', '--usage'],
                                             'primary': '--help',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'print usage and exit'},
                                         {   'aliases': ['--version'],
                                             'primary': '--version',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'show version and build info'},
                                         {   'aliases': ['-cl', '--cache-list'],
                                             'primary': '--cache-list',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'show list of models in cache'},
                                         {   'aliases': ['--completion-bash'],
                                             'primary': '--completion-bash',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'print source-able bash completion '
                                                            'script for llama.cpp'},
                                         {   'aliases': ['-t', '--threads'],
                                             'primary': '--threads',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '-1',
                                             'env': 'LLAMA_ARG_THREADS',
                                             'description': 'number of CPU threads to use during '
                                                            'generation'},
                                         {   'aliases': ['-tb', '--threads-batch'],
                                             'primary': '--threads-batch',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': 'same as --threads',
                                             'env': None,
                                             'description': 'number of threads to use during batch '
                                                            'and prompt processing'},
                                         {   'aliases': ['-C', '--cpu-mask'],
                                             'primary': '--cpu-mask',
                                             'takes_value': True,
                                             'value_hint': 'M',
                                             'choices': None,
                                             'default': '',
                                             'env': None,
                                             'description': 'CPU affinity mask: arbitrarily long '
                                                            'hex. Complements cpu-range'},
                                         {   'aliases': ['-Cr', '--cpu-range'],
                                             'primary': '--cpu-range',
                                             'takes_value': True,
                                             'value_hint': 'lo-hi',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'range of CPUs for affinity. '
                                                            'Complements --cpu-mask'},
                                         {   'aliases': ['--cpu-strict'],
                                             'primary': '--cpu-strict',
                                             'takes_value': True,
                                             'value_hint': '<0|1>',
                                             'choices': ['0', '1'],
                                             'default': '0',
                                             'env': None,
                                             'description': 'use strict CPU placement'},
                                         {   'aliases': ['--prio'],
                                             'primary': '--prio',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': ['-1', '0', '1', '2', '3'],
                                             'default': '0',
                                             'env': None,
                                             'description': 'set process/thread priority : '
                                                            'low(-1), normal(0), medium(1), '
                                                            'high(2), realtime(3)'},
                                         {   'aliases': ['--poll'],
                                             'primary': '--poll',
                                             'takes_value': True,
                                             'value_hint': '<0...100>',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'use polling level to wait for work (0 '
                                                            '- no polling)'},
                                         {   'aliases': ['-Cb', '--cpu-mask-batch'],
                                             'primary': '--cpu-mask-batch',
                                             'takes_value': True,
                                             'value_hint': 'M',
                                             'choices': None,
                                             'default': 'same as --cpu-mask',
                                             'env': None,
                                             'description': 'CPU affinity mask: arbitrarily long '
                                                            'hex. Complements cpu-range-batch'},
                                         {   'aliases': ['-Crb', '--cpu-range-batch'],
                                             'primary': '--cpu-range-batch',
                                             'takes_value': True,
                                             'value_hint': 'lo-hi',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'ranges of CPUs for affinity. '
                                                            'Complements --cpu-mask-batch'},
                                         {   'aliases': ['--cpu-strict-batch'],
                                             'primary': '--cpu-strict-batch',
                                             'takes_value': True,
                                             'value_hint': '<0|1>',
                                             'choices': ['0', '1'],
                                             'default': 'same as --cpu-strict',
                                             'env': None,
                                             'description': 'use strict CPU placement'},
                                         {   'aliases': ['--prio-batch'],
                                             'primary': '--prio-batch',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': ['0', '1', '2', '3'],
                                             'default': '0',
                                             'env': None,
                                             'description': 'set process/thread priority : '
                                                            '0-normal, 1-medium, 2-high, '
                                                            '3-realtime'},
                                         {   'aliases': ['--poll-batch'],
                                             'primary': '--poll-batch',
                                             'takes_value': True,
                                             'value_hint': '<0|1>',
                                             'choices': ['0', '1'],
                                             'default': 'same as --poll',
                                             'env': None,
                                             'description': 'use polling to wait for work'},
                                         {   'aliases': ['-c', '--ctx-size'],
                                             'primary': '--ctx-size',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '0',
                                             'env': 'LLAMA_ARG_CTX_SIZE',
                                             'description': 'size of the prompt context (default: '
                                                            '0, 0 = loaded from model)'},
                                         {   'aliases': ['-n', '--predict', '--n-predict'],
                                             'primary': '--predict',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_N_PREDICT',
                                             'description': 'number of tokens to predict'},
                                         {   'aliases': ['-b', '--batch-size'],
                                             'primary': '--batch-size',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '2048',
                                             'env': 'LLAMA_ARG_BATCH',
                                             'description': 'logical maximum batch size'},
                                         {   'aliases': ['-ub', '--ubatch-size'],
                                             'primary': '--ubatch-size',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '512',
                                             'env': 'LLAMA_ARG_UBATCH',
                                             'description': 'physical maximum batch size'},
                                         {   'aliases': ['--keep'],
                                             'primary': '--keep',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '0',
                                             'env': None,
                                             'description': 'number of tokens to keep from the '
                                                            'initial prompt'},
                                         {   'aliases': ['--swa-full'],
                                             'primary': '--swa-full',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_SWA_FULL',
                                             'description': 'use full-size SWA cache'},
                                         {   'aliases': ['-fa', '--flash-attn'],
                                             'primary': '--flash-attn',
                                             'takes_value': True,
                                             'value_hint': '<on|off|auto>',
                                             'choices': ['on', 'off', 'auto'],
                                             'default': 'auto',
                                             'env': 'LLAMA_ARG_FLASH_ATTN',
                                             'description': "set Flash Attention use ('on', 'off', "
                                                            "or 'auto', default: 'auto')"},
                                         {   'aliases': ['--perf', '--no-perf'],
                                             'primary': '--perf',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_PERF',
                                             'description': 'whether to enable internal libllama '
                                                            'performance timings'},
                                         {   'aliases': ['-e', '--escape', '--no-escape'],
                                             'primary': '--escape',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'whether to process escapes sequences '
                                                            '(\\n, \\r, \\t, \\\' , \\" , \\\\)'},
                                         {   'aliases': ['--rope-scaling'],
                                             'primary': '--rope-scaling',
                                             'takes_value': True,
                                             'value_hint': '<none,linear,yarn>',
                                             'choices': ['none', 'linear', 'yarn'],
                                             'default': 'linear',
                                             'env': 'LLAMA_ARG_ROPE_SCALING_TYPE',
                                             'description': 'RoPE frequency scaling method, '
                                                            'defaults to linear unless specified '
                                                            'by the model'},
                                         {   'aliases': ['--rope-scale'],
                                             'primary': '--rope-scale',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_ROPE_SCALE',
                                             'description': 'RoPE context scaling factor, expands '
                                                            'context by a factor of N'},
                                         {   'aliases': ['--rope-freq-base'],
                                             'primary': '--rope-freq-base',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': 'loaded from model',
                                             'env': 'LLAMA_ARG_ROPE_FREQ_BASE',
                                             'description': 'RoPE base frequency, used by '
                                                            'NTK-aware scaling'},
                                         {   'aliases': ['--rope-freq-scale'],
                                             'primary': '--rope-freq-scale',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_ROPE_FREQ_SCALE',
                                             'description': 'RoPE frequency scaling factor, '
                                                            'expands context by a factor of 1/N'},
                                         {   'aliases': ['--yarn-orig-ctx'],
                                             'primary': '--yarn-orig-ctx',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '0',
                                             'env': 'LLAMA_ARG_YARN_ORIG_CTX',
                                             'description': 'YaRN: original context size of model'},
                                         {   'aliases': ['--yarn-ext-factor'],
                                             'primary': '--yarn-ext-factor',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_YARN_EXT_FACTOR',
                                             'description': 'YaRN: extrapolation mix factor (0.0 = '
                                                            'full interpolation)'},
                                         {   'aliases': ['--yarn-attn-factor'],
                                             'primary': '--yarn-attn-factor',
                                             'takes_value': True,
                                             'value_hint': '<N>',
                                             'choices': None,
                                             'default': '-1.00',
                                             'env': 'LLAMA_ARG_YARN_ATTN_FACTOR',
                                             'description': 'YaRN: scale sqrt(t) or attention '
                                                            'magnitude'},
                                         {   'aliases': ['--yarn-beta-slow'],
                                             'primary': '--yarn-beta-slow',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '-1.00',
                                             'env': 'LLAMA_ARG_YARN_BETA_SLOW',
                                             'description': 'YaRN: high correction dim or alpha'},
                                         {   'aliases': ['--yarn-beta-fast'],
                                             'primary': '--yarn-beta-fast',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '-1.00',
                                             'env': 'LLAMA_ARG_YARN_BETA_FAST',
                                             'description': 'YaRN: low correction dim or beta'},
                                         {   'aliases': [   '-kvo',
                                                            '--kv-offload',
                                                            '-nkvo',
                                                            '--no-kv-offload'],
                                             'primary': '--kv-offload',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_KV_OFFLOAD',
                                             'description': 'whether to enable KV cache '
                                                            'offloading'},
                                         {   'aliases': ['--repack', '-nr', '--no-repack'],
                                             'primary': '--repack',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': 'enabled',
                                             'env': 'LLAMA_ARG_REPACK',
                                             'description': 'whether to enable weight repacking'},
                                         {   'aliases': ['--no-host'],
                                             'primary': '--no-host',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_NO_HOST',
                                             'description': 'bypass host buffer allowing extra '
                                                            'buffers to be used'},
                                         {   'aliases': ['-ctk', '--cache-type-k'],
                                             'primary': '--cache-type-k',
                                             'takes_value': True,
                                             'value_hint': '<TYPE>',
                                             'choices': [   'f32',
                                                            'f16',
                                                            'bf16',
                                                            'q8_0',
                                                            'q4_0',
                                                            'q4_1',
                                                            'iq4_nl',
                                                            'q5_0',
                                                            'q5_1'],
                                             'default': 'f16',
                                             'env': 'LLAMA_ARG_CACHE_TYPE_K',
                                             'description': 'KV cache data type for K'},
                                         {   'aliases': ['-ctv', '--cache-type-v'],
                                             'primary': '--cache-type-v',
                                             'takes_value': True,
                                             'value_hint': 'TYPE',
                                             'choices': [   'f32',
                                                            'f16',
                                                            'bf16',
                                                            'q8_0',
                                                            'q4_0',
                                                            'q4_1',
                                                            'iq4_nl',
                                                            'q5_0',
                                                            'q5_1'],
                                             'default': 'f16',
                                             'env': 'LLAMA_ARG_CACHE_TYPE_V',
                                             'description': 'KV cache data type for V'},
                                         {   'aliases': ['-dt', '--defrag-thold'],
                                             'primary': '--defrag-thold',
                                             'takes_value': True,
                                             'value_hint': '<N>',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_DEFRAG_THOLD',
                                             'description': 'KV cache defragmentation threshold '
                                                            '(DEPRECATED)'},
                                         {   'aliases': ['--mlock'],
                                             'primary': '--mlock',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_MLOCK',
                                             'description': 'DEPRECATED in favor of `--load-mode`: '
                                                            'force system to keep model in RAM '
                                                            'rather than swapping or compressing'},
                                         {   'aliases': ['--mmap', '--no-mmap'],
                                             'primary': '--mmap',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_MMAP',
                                             'description': 'DEPRECATED in favor of `--load-mode`: '
                                                            'whether to memory-map model. (if mmap '
                                                            'disabled, slower load but may reduce '
                                                            'pageouts if not using mlock)'},
                                         {   'aliases': [   '-dio',
                                                            '--direct-io',
                                                            '-ndio',
                                                            '--no-direct-io'],
                                             'primary': '--direct-io',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_DIO',
                                             'description': 'DEPRECATED in favor of `--load-mode`: '
                                                            'use DirectIO if available'},
                                         {   'aliases': ['-lm', '--load-mode'],
                                             'primary': '--load-mode',
                                             'takes_value': True,
                                             'value_hint': 'MODE',
                                             'choices': [   'auto',
                                                            'none',
                                                            'mmap',
                                                            'mlock',
                                                            'mmap+mlock',
                                                            'dio'],
                                             'default': 'auto',
                                             'env': 'LLAMA_ARG_LOAD_MODE',
                                             'description': 'model loading mode'},
                                         {   'aliases': ['--numa'],
                                             'primary': '--numa',
                                             'takes_value': True,
                                             'value_hint': 'TYPE',
                                             'choices': ['distribute', 'isolate', 'numactl'],
                                             'default': None,
                                             'env': 'LLAMA_ARG_NUMA',
                                             'description': 'attempt optimizations that help on '
                                                            'some NUMA systems\n'
                                                            '- distribute: spread execution evenly '
                                                            'over all nodes\n'
                                                            '- isolate: only spawn threads on CPUs '
                                                            'on the node that execution started '
                                                            'on\n'
                                                            '- numactl: use the CPU map provided '
                                                            'by numactl\n'
                                                            'if run without this previously, it is '
                                                            'recommended to drop the system page '
                                                            'cache before using this\n'
                                                            'see '
                                                            'https://github.com/ggml-org/llama.cpp/issues/1437'},
                                         {   'aliases': ['-dev', '--device'],
                                             'primary': '--device',
                                             'takes_value': True,
                                             'value_hint': '<dev1,dev2,..>',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_DEVICE',
                                             'description': 'comma-separated list of devices to '
                                                            "use for offloading (none = don't "
                                                            'offload) use --list-devices to see a '
                                                            'list of available devices'},
                                         {   'aliases': ['--list-devices'],
                                             'primary': '--list-devices',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'print list of available devices and '
                                                            'exit'},
                                         {   'aliases': ['-ot', '--override-tensor'],
                                             'primary': '--override-tensor',
                                             'takes_value': True,
                                             'value_hint': '<tensor name pattern>=<buffer '
                                                           'type>,...',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_OVERRIDE_TENSOR',
                                             'description': 'override tensor buffer type'},
                                         {   'aliases': ['-cmoe', '--cpu-moe'],
                                             'primary': '--cpu-moe',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_CPU_MOE',
                                             'description': 'keep all Mixture of Experts (MoE) '
                                                            'weights in the CPU'},
                                         {   'aliases': ['-ncmoe', '--n-cpu-moe'],
                                             'primary': '--n-cpu-moe',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_N_CPU_MOE',
                                             'description': 'keep the Mixture of Experts (MoE) '
                                                            'weights of the first N layers in the '
                                                            'CPU'},
                                         {   'aliases': ['-ngl', '--gpu-layers', '--n-gpu-layers'],
                                             'primary': '--gpu-layers',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': ['auto', 'all'],
                                             'default': 'auto',
                                             'env': 'LLAMA_ARG_N_GPU_LAYERS',
                                             'description': 'max. number of layers to store in '
                                                            'VRAM, either an exact number'},
                                         {   'aliases': ['-sm', '--split-mode'],
                                             'primary': '--split-mode',
                                             'takes_value': True,
                                             'value_hint': '{none,layer,row,tensor}',
                                             'choices': ['none', 'layer', 'row', 'tensor'],
                                             'default': 'layer',
                                             'env': 'LLAMA_ARG_SPLIT_MODE',
                                             'description': 'how to split the model across '
                                                            'multiple GPUs, one of: - none: use '
                                                            'one GPU only - layer (default): split '
                                                            'layers and KV across GPUs (pipelined) '
                                                            '- row: split weight across GPUs by '
                                                            'rows (parallelized) - tensor: split '
                                                            'weights and KV across GPUs '
                                                            '(parallelized, EXPERIMENTAL)'},
                                         {   'aliases': ['-ts', '--tensor-split'],
                                             'primary': '--tensor-split',
                                             'takes_value': True,
                                             'value_hint': '<N0,N1,N2,...>',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'fraction of the model to offload to '
                                                            'each GPU, comma-separated list of '
                                                            'proportions, e.g. 3,1'},
                                         {   'aliases': [],
                                             'primary': '--main-gpu',
                                             'takes_value': True,
                                             'value_hint': 'INDEX',
                                             'choices': None,
                                             'default': '0',
                                             'env': 'LLAMA_ARG_MAIN_GPU',
                                             'description': 'the GPU to use for the model (with '
                                                            'split-mode = none), or for '
                                                            'intermediate results and KV (with '
                                                            'split-mode = row)'},
                                         {   'aliases': ['-fit', '--fit'],
                                             'primary': '--fit',
                                             'takes_value': True,
                                             'value_hint': '<on|off>',
                                             'choices': ['on', 'off'],
                                             'default': 'on',
                                             'env': 'LLAMA_ARG_FIT',
                                             'description': 'whether to adjust unset arguments to '
                                                            "fit in device memory ('on' or 'off', "
                                                            "default: 'on')"},
                                         {   'aliases': ['-fitt', '--fit-target'],
                                             'primary': '--fit-target',
                                             'takes_value': True,
                                             'value_hint': 'MiB0,MiB1,MiB2,...',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_FIT_TARGET',
                                             'description': 'target margin per device for --fit, '
                                                            'comma-separated list of values, '
                                                            'single value is broadcast across all '
                                                            'devices'},
                                         {   'aliases': ['-fitc', '--fit-ctx'],
                                             'primary': '--fit-ctx',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': '4096',
                                             'env': 'LLAMA_ARG_FIT_CTX',
                                             'description': 'minimum ctx size that can be set by '
                                                            '--fit option'},
                                         {   'aliases': ['--check-tensors'],
                                             'primary': '--check-tensors',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'check model tensor data for invalid '
                                                            'values'},
                                         {   'aliases': ['--override-kv'],
                                             'primary': '--override-kv',
                                             'takes_value': True,
                                             'value_hint': 'KEY=TYPE:VALUE,...',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'advanced option to override model '
                                                            'metadata by key. to specify multiple '
                                                            'overrides, either use comma-separated '
                                                            'values. types: int, float, bool, str. '
                                                            'example: --override-kv '
                                                            'tokenizer.ggml.add_bos_token=bool:false,tokenizer.ggml.add_eos_token=bool:false'},
                                         {   'aliases': ['--op-offload', '--no-op-offload'],
                                             'primary': '--op-offload',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': 'true',
                                             'env': None,
                                             'description': 'whether to offload host tensor '
                                                            'operations to device'},
                                         {   'aliases': ['--lora'],
                                             'primary': '--lora',
                                             'takes_value': True,
                                             'value_hint': 'FNAME',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'path to LoRA adapter (use '
                                                            'comma-separated values to load '
                                                            'multiple adapters)'},
                                         {   'aliases': ['--lora-scaled'],
                                             'primary': '--lora-scaled',
                                             'takes_value': True,
                                             'value_hint': 'FNAME:SCALE,...',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'path to LoRA adapter with user '
                                                            'defined scaling (format: '
                                                            'FNAME:SCALE,...) note: use '
                                                            'comma-separated values'},
                                         {   'aliases': ['--control-vector'],
                                             'primary': '--control-vector',
                                             'takes_value': True,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'add a control vector note: use '
                                                            'comma-separated values to add '
                                                            'multiple control vectors'},
                                         {   'aliases': ['--control-vector-scaled'],
                                             'primary': '--control-vector-scaled',
                                             'takes_value': True,
                                             'value_hint': 'FNAME:SCALE,...',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'add a control vector with user '
                                                            'defined scaling SCALE note: use '
                                                            'comma-separated values (format: '
                                                            'FNAME:SCALE,...)'},
                                         {   'aliases': ['--control-vector-layer-range'],
                                             'primary': '--control-vector-layer-range',
                                             'takes_value': True,
                                             'value_hint': '<START> <END>',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'layer range to apply the control '
                                                            'vector(s) to, start and end '
                                                            'inclusive'},
                                         {   'aliases': ['-m', '--model'],
                                             'primary': '--model',
                                             'takes_value': True,
                                             'value_hint': 'FNAME',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_MODEL',
                                             'description': 'model path to load'},
                                         {   'aliases': ['-mu', '--model-url'],
                                             'primary': '--model-url',
                                             'takes_value': True,
                                             'value_hint': 'MODEL_URL',
                                             'choices': None,
                                             'default': 'unused',
                                             'env': 'LLAMA_ARG_MODEL_URL',
                                             'description': 'model download url'},
                                         {   'aliases': ['-dr', '--docker-repo'],
                                             'primary': '--docker-repo',
                                             'takes_value': True,
                                             'value_hint': '[<repo>/]<model>[:quant]',
                                             'choices': None,
                                             'default': 'unused',
                                             'env': 'LLAMA_ARG_DOCKER_REPO',
                                             'description': 'Docker Hub model repository. repo is '
                                                            'optional, default to ai/. quant is '
                                                            'optional, default to :latest. '
                                                            'example: gemma3'},
                                         {   'aliases': ['-hf', '-hfr', '--hf-repo'],
                                             'primary': '--hf-repo',
                                             'takes_value': True,
                                             'value_hint': '<user>/<model>[:quant]',
                                             'choices': None,
                                             'default': 'unused',
                                             'env': 'LLAMA_ARG_HF_REPO',
                                             'description': 'Hugging Face model repository; quant '
                                                            'is optional, case-insensitive, '
                                                            'default to Q4_K_M, or falls back to '
                                                            'the first file in the repo if Q4_K_M '
                                                            "doesn't exist. mmproj is also "
                                                            'downloaded automatically if '
                                                            'available. to disable, add '
                                                            '--no-mmproj example: '
                                                            'ggml-org/GLM-4.7-Flash-GGUF:Q4_K_M '
                                                            '(default: unused)'},
                                         {   'aliases': ['-hff', '--hf-file'],
                                             'primary': '--hf-file',
                                             'takes_value': True,
                                             'value_hint': 'FILE',
                                             'choices': None,
                                             'default': 'unused',
                                             'env': 'LLAMA_ARG_HF_FILE',
                                             'description': 'Hugging Face model file. If '
                                                            'specified, it will override the quant '
                                                            'in --hf-repo (default: unused)'},
                                         {   'aliases': ['-hft', '--hf-token'],
                                             'primary': '--hf-token',
                                             'takes_value': True,
                                             'value_hint': 'TOKEN',
                                             'choices': None,
                                             'default': 'value from HF_TOKEN environment variable',
                                             'env': 'HF_TOKEN',
                                             'description': 'Hugging Face access token'},
                                         {   'aliases': ['--log-disable'],
                                             'primary': '--log-disable',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'Log disable'},
                                         {   'aliases': ['--log-file'],
                                             'primary': '--log-file',
                                             'takes_value': True,
                                             'value_hint': 'FNAME',
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_LOG_FILE',
                                             'description': 'Log to file'},
                                         {   'aliases': ['--log-colors'],
                                             'primary': '--log-colors',
                                             'takes_value': True,
                                             'value_hint': '<on|off|auto>',
                                             'choices': ['on', 'off', 'auto'],
                                             'default': 'auto',
                                             'env': 'LLAMA_ARG_LOG_COLORS',
                                             'description': "Set colored logging ('on', 'off', or "
                                                            "'auto', default: 'auto'). 'auto' "
                                                            'enables colors when output is to a '
                                                            'terminal.'},
                                         {   'aliases': ['-v', '--verbose', '--log-verbose'],
                                             'primary': '--verbose',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'Set verbosity level to infinity (i.e. '
                                                            'log all messages, useful for '
                                                            'debugging)'},
                                         {   'aliases': ['--offline'],
                                             'primary': '--offline',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_OFFLINE',
                                             'description': 'Offline mode: forces use of cache, '
                                                            'prevents network access'},
                                         {   'aliases': ['-lv', '--verbosity', '--log-verbosity'],
                                             'primary': '--verbosity',
                                             'takes_value': True,
                                             'value_hint': 'N',
                                             'choices': None,
                                             'default': None,
                                             'env': None,
                                             'description': 'Set the verbosity threshold. Messages '
                                                            'with a higher verbosity will be '
                                                            'ignored.'},
                                         {   'aliases': ['--log-prefix', '--no-log-prefix'],
                                             'primary': '--log-prefix',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_LOG_PREFIX',
                                             'description': 'Enable prefix in log messages'},
                                         {   'aliases': ['--log-timestamps', '--no-log-timestamps'],
                                             'primary': '--log-timestamps',
                                             'takes_value': False,
                                             'value_hint': None,
                                             'choices': None,
                                             'default': None,
                                             'env': 'LLAMA_ARG_LOG_TIMESTAMPS',
                                             'description': 'Enable timestamps in log messages'},
                                         {   'aliases': [   '--spec-draft-type-k',
                                                            '-ctkd',
                                                            '--cache-type-k-draft'],
                                             'primary': '--spec-draft-type-k',
                                             'takes_value': True,
                                             'value_hint': 'TYPE',
                                             'choices': [   'f32',
                                                            'f16',
                                                            'bf16',
                                                            'q8_0',
                                                            'q4_0',
                                                            'q4_1',
                                                            'iq4_nl',
                                                            'q5_0',
                                                            'q5_1'],
                                             'default': 'f16',
                                             'env': 'LLAMA_ARG_SPEC_DRAFT_CACHE_TYPE_K',
                                             'description': 'KV cache data type for K for the '
                                                            'draft model'},
                                         {   'aliases': [   '--spec-draft-type-v',
                                                            '-ctvd',
                                                            '--cache-type-v-draft'],
                                             'primary': '--spec-draft-type-v',
                                             'takes_value': True,
                                             'value_hint': 'TYPE',
                                             'choices': [   'f32',
                                                            'f16',
                                                            'bf16',
                                                            'q8_0',
                                                            'q4_0',
                                                            'q4_1',
                                                            'iq4_nl',
                                                            'q5_0',
                                                            'q5_1'],
                                             'default': 'f16',
                                             'env': 'LLAMA_ARG_SPEC_DRAFT_CACHE_TYPE_V',
                                             'description': 'KV cache data type for V for the '
                                                            'draft model'}],
                    'sampling params': [   {   'aliases': ['--samplers'],
                                               'primary': '--samplers',
                                               'takes_value': True,
                                               'value_hint': '<SAMPLERS>',
                                               'choices': None,
                                               'default': 'penalties;dry;top_n_sigma;top_k;typ_p;top_p;min_p;xtc;temperature',
                                               'env': None,
                                               'description': 'samplers that will be used for '
                                                              'generation in the order, separated '
                                                              "by ';'"},
                                           {   'aliases': ['-s', '--seed'],
                                               'primary': '--seed',
                                               'takes_value': True,
                                               'value_hint': 'SEED',
                                               'choices': None,
                                               'default': '-1',
                                               'env': None,
                                               'description': 'RNG seed'},
                                           {   'aliases': ['--sampler-seq', '--sampling-seq'],
                                               'primary': '--sampler-seq',
                                               'takes_value': True,
                                               'value_hint': 'SEQUENCE',
                                               'choices': None,
                                               'default': 'edskypmxt',
                                               'env': None,
                                               'description': 'simplified sequence for samplers '
                                                              'that will be used'},
                                           {   'aliases': ['--ignore-eos'],
                                               'primary': '--ignore-eos',
                                               'takes_value': False,
                                               'value_hint': None,
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'ignore end of stream token and '
                                                              'continue generating (implies '
                                                              '--logit-bias EOS-inf)'},
                                           {   'aliases': ['--temp', '--temperature'],
                                               'primary': '--temp',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.80',
                                               'env': None,
                                               'description': 'temperature'},
                                           {   'aliases': ['--top-k'],
                                               'primary': '--top-k',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '40',
                                               'env': 'LLAMA_ARG_TOP_K',
                                               'description': 'top-k sampling (0 = disabled)'},
                                           {   'aliases': ['--top-p'],
                                               'primary': '--top-p',
                                               'takes_value': True,
                                               'value_hint': '<N>',
                                               'choices': None,
                                               'default': '0.95',
                                               'env': None,
                                               'description': 'top-p sampling'},
                                           {   'aliases': ['--min-p'],
                                               'primary': '--min-p',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'min-p sampling (0.0 = disabled)'},
                                           {   'aliases': ['--top-nsigma', '--top-n-sigma'],
                                               'primary': '--top-nsigma',
                                               'takes_value': True,
                                               'value_hint': '<N>',
                                               'choices': None,
                                               'default': '-1.00',
                                               'env': None,
                                               'description': 'top-n-sigma sampling'},
                                           {   'aliases': ['--xtc-probability'],
                                               'primary': '--xtc-probability',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.00',
                                               'env': None,
                                               'description': 'xtc probability (default: 0.00, 0.0 '
                                                              '= disabled)'},
                                           {   'aliases': ['--xtc-threshold'],
                                               'primary': '--xtc-threshold',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.10',
                                               'env': None,
                                               'description': 'xtc threshold (1.0 = disabled)'},
                                           {   'aliases': ['--typical', '--typical-p'],
                                               'primary': '--typical',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '1.00',
                                               'env': None,
                                               'description': 'locally typical sampling, parameter '
                                                              'p'},
                                           {   'aliases': ['--repeat-last-n'],
                                               'primary': '--repeat-last-n',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'last n tokens to consider for '
                                                              'penalize'},
                                           {   'aliases': ['--repeat-penalty'],
                                               'primary': '--repeat-penalty',
                                               'takes_value': True,
                                               'value_hint': '<N>',
                                               'choices': None,
                                               'default': '1.00',
                                               'env': None,
                                               'description': 'penalize repeat sequence of tokens'},
                                           {   'aliases': ['--presence-penalty'],
                                               'primary': '--presence-penalty',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.00',
                                               'env': None,
                                               'description': 'repeat alpha presence penalty (0.0 '
                                                              '= disabled)'},
                                           {   'aliases': ['--frequency-penalty'],
                                               'primary': '--frequency-penalty',
                                               'takes_value': True,
                                               'value_hint': '<N>',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'repeat alpha frequency penalty (0.0 '
                                                              '= disabled)'},
                                           {   'aliases': ['--dry-multiplier'],
                                               'primary': '--dry-multiplier',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.00',
                                               'env': None,
                                               'description': 'set DRY sampling multiplier (0.0 = '
                                                              'disabled)'},
                                           {   'aliases': ['--dry-base'],
                                               'primary': '--dry-base',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '1.75',
                                               'env': None,
                                               'description': 'set DRY sampling base value'},
                                           {   'aliases': ['--dry-allowed-length'],
                                               'primary': '--dry-allowed-length',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '2',
                                               'env': None,
                                               'description': 'set allowed length for DRY '
                                                              'sampling'},
                                           {   'aliases': ['--dry-penalty-last-n'],
                                               'primary': '--dry-penalty-last-n',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'set DRY penalty for the last n '
                                                              'tokens (0 = disable)'},
                                           {   'aliases': ['--dry-sequence-breaker'],
                                               'primary': '--dry-sequence-breaker',
                                               'takes_value': True,
                                               'value_hint': 'STRING',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'add sequence breaker for DRY '
                                                              'sampling, clearing out default '
                                                              'breakers (\'\\n\', \':\', \'"\', '
                                                              '\'*\') in the process; use "none" '
                                                              'to not use any sequence breakers'},
                                           {   'aliases': ['--adaptive-target'],
                                               'primary': '--adaptive-target',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '-1.00',
                                               'env': None,
                                               'description': 'adaptive-p: select tokens near this '
                                                              'probability (valid range 0.0 to '
                                                              '1.0; negative = disabled)'},
                                           {   'aliases': ['--adaptive-decay'],
                                               'primary': '--adaptive-decay',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.90',
                                               'env': None,
                                               'description': 'adaptive-p: decay rate for target '
                                                              'adaptation over time. lower values '
                                                              'are more reactive, higher values '
                                                              'are more stable. (valid range 0.0 '
                                                              'to 0.99)'},
                                           {   'aliases': ['--dynatemp-range'],
                                               'primary': '--dynatemp-range',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.00',
                                               'env': None,
                                               'description': 'dynamic temperature range (0.0 = '
                                                              'disabled)'},
                                           {   'aliases': ['--dynatemp-exp'],
                                               'primary': '--dynatemp-exp',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '1.00',
                                               'env': None,
                                               'description': 'dynamic temperature exponent'},
                                           {   'aliases': ['--mirostat'],
                                               'primary': '--mirostat',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': ['0', '1', '2'],
                                               'default': '0',
                                               'env': None,
                                               'description': 'use Mirostat sampling. Top K, '
                                                              'Nucleus and Locally Typical '
                                                              'samplers are ignored if used.'},
                                           {   'aliases': ['--mirostat-lr'],
                                               'primary': '--mirostat-lr',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '0.10',
                                               'env': None,
                                               'description': 'Mirostat learning rate, parameter '
                                                              'eta'},
                                           {   'aliases': ['--mirostat-ent'],
                                               'primary': '--mirostat-ent',
                                               'takes_value': True,
                                               'value_hint': 'N',
                                               'choices': None,
                                               'default': '5.00',
                                               'env': None,
                                               'description': 'Mirostat target entropy, parameter '
                                                              'tau'},
                                           {   'aliases': ['-l', '--logit-bias'],
                                               'primary': '--logit-bias',
                                               'takes_value': True,
                                               'value_hint': 'TOKEN_ID(+/-)BIAS',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'modifies the likelihood of token '
                                                              'appearing in the completion, i.e. '
                                                              '`--logit-bias 15043+1` to increase '
                                                              "likelihood of token ' Hello', or "
                                                              '`--logit-bias 15043-1` to decrease '
                                                              "likelihood of token ' Hello'"},
                                           {   'aliases': ['--grammar'],
                                               'primary': '--grammar',
                                               'takes_value': True,
                                               'value_hint': 'GRAMMAR',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'BNF-like grammar to constrain '
                                                              'generations (see samples in '
                                                              'grammars/ dir)'},
                                           {   'aliases': ['--grammar-file'],
                                               'primary': '--grammar-file',
                                               'takes_value': True,
                                               'value_hint': 'FNAME',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'file to read grammar from'},
                                           {   'aliases': ['-j', '--json-schema'],
                                               'primary': '--json-schema',
                                               'takes_value': True,
                                               'value_hint': 'SCHEMA',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'JSON schema to constrain '
                                                              'generations '
                                                              '(https://json-schema.org/), e.g. '
                                                              '`{}` for any JSON object For '
                                                              'schemas w/ external $refs, use '
                                                              '--grammar + '
                                                              'example/json_schema_to_grammar.py '
                                                              'instead'},
                                           {   'aliases': ['-jf', '--json-schema-file'],
                                               'primary': '--json-schema-file',
                                               'takes_value': True,
                                               'value_hint': 'FILE',
                                               'choices': None,
                                               'default': None,
                                               'env': None,
                                               'description': 'File containing a JSON schema to '
                                                              'constrain generations '
                                                              '(https://json-schema.org/), e.g. '
                                                              '`{}` for any JSON object For '
                                                              'schemas w/ external $refs, use '
                                                              '--grammar + '
                                                              'example/json_schema_to_grammar.py '
                                                              'instead'},
                                           {   'aliases': ['-bs', '--backend-sampling'],
                                               'primary': '--backend-sampling',
                                               'takes_value': False,
                                               'value_hint': None,
                                               'choices': None,
                                               'default': 'disabled',
                                               'env': 'LLAMA_ARG_BACKEND_SAMPLING',
                                               'description': 'enable backend sampling '
                                                              '(experimental)'}],
                    'speculative params': [   {   'aliases': [],
                                                  'primary': '--spec-draft-hf',
                                                  'takes_value': True,
                                                  'value_hint': '<user>/<model>[:quant]',
                                                  'choices': None,
                                                  'default': 'unused',
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_HF_REPO',
                                                  'description': 'Same as --hf-repo, but for the '
                                                                 'draft model'},
                                              {   'aliases': [   '--spec-draft-threads',
                                                                 '-td',
                                                                 '--threads-draft'],
                                                  'primary': '--spec-draft-threads',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': 'same as --threads',
                                                  'env': None,
                                                  'description': 'number of threads to use during '
                                                                 'generation (default: same as '
                                                                 '--threads)'},
                                              {   'aliases': [   '--spec-draft-threads-batch',
                                                                 '-tbd',
                                                                 '--threads-batch-draft'],
                                                  'primary': '--spec-draft-threads-batch',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': 'same as --threads-draft',
                                                  'env': None,
                                                  'description': 'number of threads to use during '
                                                                 'batch and prompt processing '
                                                                 '(default: same as '
                                                                 '--threads-draft)'},
                                              {   'aliases': [   '--spec-draft-cpu-mask',
                                                                 '-Cd',
                                                                 '--cpu-mask-draft'],
                                                  'primary': '--spec-draft-cpu-mask',
                                                  'takes_value': True,
                                                  'value_hint': 'M',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'Draft model CPU affinity mask. '
                                                                 'Complements cpu-range-draft '
                                                                 '(default: same as --cpu-mask)'},
                                              {   'aliases': [   '--spec-draft-cpu-range',
                                                                 '-Crd',
                                                                 '--cpu-range-draft'],
                                                  'primary': '--spec-draft-cpu-range',
                                                  'takes_value': True,
                                                  'value_hint': 'lo-hi',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'Ranges of CPUs for affinity. '
                                                                 'Complements --cpu-mask-draft'},
                                              {   'aliases': [   '--spec-draft-cpu-strict',
                                                                 '--cpu-strict-draft'],
                                                  'primary': '--spec-draft-cpu-strict',
                                                  'takes_value': True,
                                                  'value_hint': '<0|1>',
                                                  'choices': ['0', '1'],
                                                  'default': 'same as --cpu-strict',
                                                  'env': None,
                                                  'description': 'Use strict CPU placement for '
                                                                 'draft model'},
                                              {   'aliases': ['--spec-draft-prio', '--prio-draft'],
                                                  'primary': '--spec-draft-prio',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': ['0', '1', '2', '3'],
                                                  'default': '0',
                                                  'env': None,
                                                  'description': 'set draft process/thread '
                                                                 'priority : 0-normal, 1-medium, '
                                                                 '2-high, 3-realtime'},
                                              {   'aliases': ['--spec-draft-poll', '--poll-draft'],
                                                  'primary': '--spec-draft-poll',
                                                  'takes_value': True,
                                                  'value_hint': '<0|1>',
                                                  'choices': ['0', '1'],
                                                  'default': 'same as --poll',
                                                  'env': None,
                                                  'description': 'Use polling to wait for draft '
                                                                 'model work (default: same as '
                                                                 '--poll)'},
                                              {   'aliases': [   '--spec-draft-cpu-mask-batch',
                                                                 '-Cbd',
                                                                 '--cpu-mask-batch-draft'],
                                                  'primary': '--spec-draft-cpu-mask-batch',
                                                  'takes_value': True,
                                                  'value_hint': '<M>',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'Draft model CPU affinity mask. '
                                                                 'Complements cpu-range-draft '
                                                                 '(default: same as --cpu-mask)'},
                                              {   'aliases': [   '--spec-draft-cpu-strict-batch',
                                                                 '--cpu-strict-batch-draft'],
                                                  'primary': '--spec-draft-cpu-strict-batch',
                                                  'takes_value': True,
                                                  'value_hint': '<0|1>',
                                                  'choices': ['0', '1'],
                                                  'default': '--cpu-strict-draft',
                                                  'env': None,
                                                  'description': 'Use strict CPU placement for '
                                                                 'draft model'},
                                              {   'aliases': [   '--spec-draft-prio-batch',
                                                                 '--prio-batch-draft'],
                                                  'primary': '--spec-draft-prio-batch',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': ['0', '1', '2', '3'],
                                                  'default': '0',
                                                  'env': None,
                                                  'description': 'set draft process/thread '
                                                                 'priority : 0-normal, 1-medium, '
                                                                 '2-high, 3-realtime'},
                                              {   'aliases': [   '--spec-draft-poll-batch',
                                                                 '--poll-batch-draft'],
                                                  'primary': '--spec-draft-poll-batch',
                                                  'takes_value': True,
                                                  'value_hint': '<0|1>',
                                                  'choices': ['0', '1'],
                                                  'default': '--poll-draft',
                                                  'env': None,
                                                  'description': 'Use polling to wait for draft '
                                                                 'model work'},
                                              {   'aliases': [   '--spec-draft-override-tensor',
                                                                 '-otd',
                                                                 '--override-draft-tensor'],
                                                  'primary': '--spec-draft-override-tensor',
                                                  'takes_value': True,
                                                  'value_hint': '<tensor name pattern>=<buffer '
                                                                'type>,...',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'override tensor buffer type for '
                                                                 'draft model'},
                                              {   'aliases': [   '--spec-draft-cpu-moe',
                                                                 '-cmoed',
                                                                 '--cpu-moe-draft'],
                                                  'primary': '--spec-draft-cpu-moe',
                                                  'takes_value': False,
                                                  'value_hint': None,
                                                  'choices': None,
                                                  'default': None,
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_CPU_MOE',
                                                  'description': 'keep all Mixture of Experts '
                                                                 '(MoE) weights in the CPU for the '
                                                                 'draft model'},
                                              {   'aliases': [   '--spec-draft-n-cpu-moe',
                                                                 '--spec-draft-ncmoe',
                                                                 '-ncmoed',
                                                                 '--n-cpu-moe-draft'],
                                                  'primary': '--spec-draft-n-cpu-moe',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_N_CPU_MOE',
                                                  'description': 'keep the Mixture of Experts '
                                                                 '(MoE) weights of the first N '
                                                                 'layers in the CPU for the draft '
                                                                 'model'},
                                              {   'aliases': ['--spec-draft-n-max'],
                                                  'primary': '--spec-draft-n-max',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '3',
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_N_MAX',
                                                  'description': 'number of tokens to draft for '
                                                                 'speculative decoding'},
                                              {   'aliases': ['--spec-draft-n-min'],
                                                  'primary': '--spec-draft-n-min',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '0',
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_N_MIN',
                                                  'description': 'minimum number of draft tokens '
                                                                 'to use for speculative decoding'},
                                              {   'aliases': [   '--spec-draft-p-split',
                                                                 '--draft-p-split'],
                                                  'primary': '--spec-draft-p-split',
                                                  'takes_value': True,
                                                  'value_hint': 'P',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_P_SPLIT',
                                                  'description': 'speculative decoding split '
                                                                 'probability'},
                                              {   'aliases': [   '--spec-draft-p-min',
                                                                 '--draft-p-min'],
                                                  'primary': '--spec-draft-p-min',
                                                  'takes_value': True,
                                                  'value_hint': 'P',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_P_MIN',
                                                  'description': 'minimum speculative decoding '
                                                                 'probability (greedy)'},
                                              {   'aliases': [   '--spec-draft-backend-sampling',
                                                                 '--no-spec-draft-backend-sampling'],
                                                  'primary': '--spec-draft-backend-sampling',
                                                  'takes_value': False,
                                                  'value_hint': None,
                                                  'choices': None,
                                                  'default': None,
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_BACKEND_SAMPLING',
                                                  'description': 'offload draft sampling to the '
                                                                 'backend (default: enabled)'},
                                              {   'aliases': [   '--spec-draft-device',
                                                                 '-devd',
                                                                 '--device-draft'],
                                                  'primary': '--spec-draft-device',
                                                  'takes_value': True,
                                                  'value_hint': '<dev1,dev2,..>',
                                                  'choices': ['none'],
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'comma-separated list of devices '
                                                                 'to use for offloading the draft '
                                                                 "model (none = don't offload) use "
                                                                 '--list-devices to see a list of '
                                                                 'available devices'},
                                              {   'aliases': [   '--spec-draft-ngl',
                                                                 '-ngld',
                                                                 '--gpu-layers-draft',
                                                                 '--n-gpu-layers-draft'],
                                                  'primary': '--spec-draft-ngl',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': ['auto', 'all'],
                                                  'default': 'auto',
                                                  'env': 'LLAMA_ARG_N_GPU_LAYERS_DRAFT',
                                                  'description': 'max. number of draft model '
                                                                 'layers to store in VRAM, either '
                                                                 "an exact number, 'auto', or "
                                                                 "'all' (default: auto)"},
                                              {   'aliases': [   '--spec-draft-model',
                                                                 '-md',
                                                                 '--model-draft'],
                                                  'primary': '--spec-draft-model',
                                                  'takes_value': True,
                                                  'value_hint': '<FNAME>',
                                                  'choices': None,
                                                  'default': 'unused',
                                                  'env': 'LLAMA_ARG_SPEC_DRAFT_MODEL',
                                                  'description': 'draft model for speculative '
                                                                 'decoding (default: unused)'},
                                              {   'aliases': ['--spec-type'],
                                                  'primary': '--spec-type',
                                                  'takes_value': True,
                                                  'value_hint': 'none,draft-simple,draft-eagle3,draft-mtp,draft-dflash,draft-dspark,ngram-simple,ngram-map-k,ngram-map-k4v,ngram-mod,ngram-cache',
                                                  'choices': [   'none',
                                                                 'draft-simple',
                                                                 'draft-eagle3',
                                                                 'draft-mtp',
                                                                 'draft-dflash',
                                                                 'draft-dspark',
                                                                 'ngram-simple',
                                                                 'ngram-map-k',
                                                                 'ngram-map-k4v',
                                                                 'ngram-mod',
                                                                 'ngram-cache'],
                                                  'default': 'none',
                                                  'env': 'LLAMA_ARG_SPEC_TYPE',
                                                  'description': 'comma-separated list of types of '
                                                                 'speculative decoding to use'},
                                              {   'aliases': ['--spec-ngram-mod-n-min'],
                                                  'primary': '--spec-ngram-mod-n-min',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '48',
                                                  'env': None,
                                                  'description': 'minimum number of ngram tokens '
                                                                 'to use for ngram-based '
                                                                 'speculative decoding'},
                                              {   'aliases': ['--spec-ngram-mod-n-max'],
                                                  'primary': '--spec-ngram-mod-n-max',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '64',
                                                  'env': None,
                                                  'description': 'maximum number of ngram tokens '
                                                                 'to use for ngram-based '
                                                                 'speculative decoding'},
                                              {   'aliases': ['--spec-ngram-mod-n-match'],
                                                  'primary': '--spec-ngram-mod-n-match',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '24',
                                                  'env': None,
                                                  'description': 'ngram-mod lookup length'},
                                              {   'aliases': ['--spec-ngram-simple-size-n'],
                                                  'primary': '--spec-ngram-simple-size-n',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'ngram size N for ngram-simple '
                                                                 'speculative decoding, length of '
                                                                 'lookup n-gram'},
                                              {   'aliases': ['--spec-ngram-simple-size-m'],
                                                  'primary': '--spec-ngram-simple-size-m',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '48',
                                                  'env': None,
                                                  'description': 'ngram size M for ngram-simple '
                                                                 'speculative decoding, length of '
                                                                 'draft m-gram'},
                                              {   'aliases': ['--spec-ngram-simple-min-hits'],
                                                  'primary': '--spec-ngram-simple-min-hits',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '1',
                                                  'env': None,
                                                  'description': 'minimum hits for ngram-simple '
                                                                 'speculative decoding'},
                                              {   'aliases': ['--spec-ngram-map-k-size-n'],
                                                  'primary': '--spec-ngram-map-k-size-n',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'ngram size N for ngram-map-k '
                                                                 'speculative decoding, length of '
                                                                 'lookup n-gram'},
                                              {   'aliases': ['--spec-ngram-map-k-size-m'],
                                                  'primary': '--spec-ngram-map-k-size-m',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'ngram size M for ngram-map-k '
                                                                 'speculative decoding, length of '
                                                                 'draft m-gram'},
                                              {   'aliases': ['--spec-ngram-map-k-min-hits'],
                                                  'primary': '--spec-ngram-map-k-min-hits',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '1',
                                                  'env': None,
                                                  'description': 'minimum hits for ngram-map-k '
                                                                 'speculative decoding'},
                                              {   'aliases': ['--spec-ngram-map-k4v-size-n'],
                                                  'primary': '--spec-ngram-map-k4v-size-n',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '12',
                                                  'env': None,
                                                  'description': 'ngram size N for ngram-map-k4v '
                                                                 'speculative decoding, length of '
                                                                 'lookup n-gram'},
                                              {   'aliases': [],
                                                  'primary': '--spec-ngram-map-k4v-size-m',
                                                  'takes_value': True,
                                                  'value_hint': '<N>',
                                                  'choices': None,
                                                  'default': '48',
                                                  'env': None,
                                                  'description': 'ngram size M for ngram-map-k4v '
                                                                 'speculative decoding, length of '
                                                                 'draft m-gram'},
                                              {   'aliases': ['--spec-ngram-map-k4v-min-hits'],
                                                  'primary': '--spec-ngram-map-k4v-min-hits',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': '1',
                                                  'env': None,
                                                  'description': 'minimum hits for ngram-map-k4v '
                                                                 'speculative decoding'},
                                              {   'aliases': [   '--draft',
                                                                 '--draft-n',
                                                                 '--draft-max'],
                                                  'primary': '--draft',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': 'LLAMA_ARG_DRAFT_MAX',
                                                  'description': 'the argument has been removed. '
                                                                 'use --spec-draft-n-max or '
                                                                 '--spec-ngram-mod-n-max'},
                                              {   'aliases': ['--draft-min', '--draft-n-min'],
                                                  'primary': '--draft-min',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': 'LLAMA_ARG_DRAFT_MIN',
                                                  'description': 'the argument has been removed. '
                                                                 'use --spec-draft-n-min or '
                                                                 '--spec-ngram-mod-n-min'},
                                              {   'aliases': ['--spec-ngram-size-n'],
                                                  'primary': '--spec-ngram-size-n',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'the argument has been removed. '
                                                                 'use the respective '
                                                                 '--spec-ngram-*-size-n or '
                                                                 '--spec-ngram-mod-n-match'},
                                              {   'aliases': ['--spec-ngram-size-m'],
                                                  'primary': '--spec-ngram-size-m',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'the argument has been removed. '
                                                                 'use the respective '
                                                                 '--spec-ngram-*-size-m'},
                                              {   'aliases': ['--spec-ngram-min-hits'],
                                                  'primary': '--spec-ngram-min-hits',
                                                  'takes_value': True,
                                                  'value_hint': 'N',
                                                  'choices': None,
                                                  'default': None,
                                                  'env': None,
                                                  'description': 'the argument has been removed. '
                                                                 'use the respective '
                                                                 '--spec-ngram-*-min-hits'}],
                    'example-specific params': [   {   'aliases': ['-lcs', '--lookup-cache-static'],
                                                       'primary': '--lookup-cache-static',
                                                       'takes_value': True,
                                                       'value_hint': 'FNAME',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'path to static lookup cache '
                                                                      'to use for lookup decoding '
                                                                      '(not updated by '
                                                                      'generation)'},
                                                   {   'aliases': [   '-lcd',
                                                                      '--lookup-cache-dynamic'],
                                                       'primary': '--lookup-cache-dynamic',
                                                       'takes_value': True,
                                                       'value_hint': '<file>',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'path to dynamic lookup '
                                                                      'cache to use for lookup '
                                                                      'decoding (updated by '
                                                                      'generation)'},
                                                   {   'aliases': [   '-ctxcp',
                                                                      '--ctx-checkpoints',
                                                                      '--swa-checkpoints'],
                                                       'primary': '--ctx-checkpoints',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '32',
                                                       'env': 'LLAMA_ARG_CTX_CHECKPOINTS',
                                                       'description': 'max number of context '
                                                                      'checkpoints to create per '
                                                                      'slot'},
                                                   {   'aliases': ['-cms', '--checkpoint-min-step'],
                                                       'primary': '--checkpoint-min-step',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_CHECKPOINT_MIN_SPACING_NT',
                                                       'description': 'minimum spacing between '
                                                                      'context checkpoints in '
                                                                      'tokens (default: 8192, 0 = '
                                                                      'no minimum)'},
                                                   {   'aliases': ['-cram', '--cache-ram'],
                                                       'primary': '--cache-ram',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '8192',
                                                       'env': 'LLAMA_ARG_CACHE_RAM',
                                                       'description': 'set the maximum cache size '
                                                                      'in MiB (default: 8192, -1 - '
                                                                      'no limit, 0 - '
                                                                      'disable)[(more '
                                                                      'info)](https://github.com/ggml-org/llama.cpp/pull/16391)'},
                                                   {   'aliases': [   '-kvu',
                                                                      '--kv-unified',
                                                                      '-no-kvu',
                                                                      '--no-kv-unified'],
                                                       'primary': '--kv-unified',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled if number of slots is '
                                                                  'auto',
                                                       'env': 'LLAMA_ARG_KV_UNIFIED',
                                                       'description': 'use single unified KV '
                                                                      'buffer shared across all '
                                                                      'sequences'},
                                                   {   'aliases': [   '--cache-idle-slots',
                                                                      '--no-cache-idle-slots'],
                                                       'primary': '--cache-idle-slots',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_CACHE_IDLE_SLOTS',
                                                       'description': 'save idle slots to the '
                                                                      'prompt cache on new task, '
                                                                      'and clear them when using '
                                                                      'unified KV'},
                                                   {   'aliases': [   '--context-shift',
                                                                      '--no-context-shift'],
                                                       'primary': '--context-shift',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_CONTEXT_SHIFT',
                                                       'description': 'whether to use context '
                                                                      'shift on infinite text '
                                                                      'generation (default: '
                                                                      'disabled)'},
                                                   {   'aliases': ['-r', '--reverse-prompt'],
                                                       'primary': '--reverse-prompt',
                                                       'takes_value': True,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'halt generation at PROMPT, '
                                                                      'return control in '
                                                                      'interactive mode'},
                                                   {   'aliases': ['-sp', '--special'],
                                                       'primary': '--special',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'special tokens output '
                                                                      'enabled'},
                                                   {   'aliases': ['--warmup', '--no-warmup'],
                                                       'primary': '--warmup',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled',
                                                       'env': None,
                                                       'description': 'whether to perform warmup '
                                                                      'with an empty run'},
                                                   {   'aliases': ['--spm-infill'],
                                                       'primary': '--spm-infill',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': None,
                                                       'description': 'use Suffix/Prefix/Middle '
                                                                      'pattern for infill (instead '
                                                                      'of Prefix/Suffix/Middle) as '
                                                                      'some models prefer this.'},
                                                   {   'aliases': ['--pooling'],
                                                       'primary': '--pooling',
                                                       'takes_value': True,
                                                       'value_hint': '{none,mean,cls,last,rank}',
                                                       'choices': [   'none',
                                                                      'mean',
                                                                      'cls',
                                                                      'last',
                                                                      'rank'],
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_POOLING',
                                                       'description': 'pooling type for '
                                                                      'embeddings, use model '
                                                                      'default if unspecified'},
                                                   {   'aliases': ['-np', '--parallel'],
                                                       'primary': '--parallel',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '-1',
                                                       'env': 'LLAMA_ARG_N_PARALLEL',
                                                       'description': 'number of server slots'},
                                                   {   'aliases': [   '-cb',
                                                                      '--cont-batching',
                                                                      '-nocb',
                                                                      '--no-cont-batching'],
                                                       'primary': '--cont-batching',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled',
                                                       'env': 'LLAMA_ARG_CONT_BATCHING',
                                                       'description': 'whether to enable '
                                                                      'continuous batching (a.k.a '
                                                                      'dynamic batching)'},
                                                   {   'aliases': ['-mm', '--mmproj'],
                                                       'primary': '--mmproj',
                                                       'takes_value': True,
                                                       'value_hint': '<file>',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_MMPROJ',
                                                       'description': 'path to a multimodal '
                                                                      'projector file. see '
                                                                      'tools/mtmd/README.md note: '
                                                                      'if -hf is used, this '
                                                                      'argument can be omitted'},
                                                   {   'aliases': ['-mmu', '--mmproj-url'],
                                                       'primary': '--mmproj-url',
                                                       'takes_value': True,
                                                       'value_hint': '<URL>',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'URL to a multimodal '
                                                                      'projector file. see '
                                                                      'tools/mtmd/README.md'},
                                                   {   'aliases': [   '--mmproj-auto',
                                                                      '--no-mmproj',
                                                                      '--no-mmproj-auto'],
                                                       'primary': '--mmproj-auto',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled',
                                                       'env': 'LLAMA_ARG_MMPROJ_AUTO',
                                                       'description': 'whether to use multimodal '
                                                                      'projector file (if '
                                                                      'available), useful when '
                                                                      'using -hf'},
                                                   {   'aliases': [   '--mmproj-offload',
                                                                      '--no-mmproj-offload'],
                                                       'primary': '--mmproj-offload',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled',
                                                       'env': 'LLAMA_ARG_MMPROJ_OFFLOAD',
                                                       'description': 'whether to enable GPU '
                                                                      'offloading for multimodal '
                                                                      'projector'},
                                                   {   'aliases': ['--image-min-tokens'],
                                                       'primary': '--image-min-tokens',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': 'read from model',
                                                       'env': 'LLAMA_ARG_IMAGE_MIN_TOKENS',
                                                       'description': 'minimum number of tokens '
                                                                      'each image can take, only '
                                                                      'used by vision models with '
                                                                      'dynamic resolution'},
                                                   {   'aliases': ['--image-max-tokens'],
                                                       'primary': '--image-max-tokens',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': 'read from model',
                                                       'env': 'LLAMA_ARG_IMAGE_MAX_TOKENS',
                                                       'description': 'maximum number of tokens '
                                                                      'each image can take, only '
                                                                      'used by vision models with '
                                                                      'dynamic resolution'},
                                                   {   'aliases': ['--mtmd-batch-max-tokens'],
                                                       'primary': '--mtmd-batch-max-tokens',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '1024',
                                                       'env': 'LLAMA_ARG_MTMD_BATCH_MAX_TOKENS',
                                                       'description': 'maximum number of image '
                                                                      'tokens per batch when '
                                                                      'encoding images'},
                                                   {   'aliases': ['-a', '--alias'],
                                                       'primary': '--alias',
                                                       'takes_value': True,
                                                       'value_hint': 'STRING',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_ALIAS',
                                                       'description': 'set model name aliases, '
                                                                      'comma-separated (to be used '
                                                                      'by API)'},
                                                   {   'aliases': [],
                                                       'primary': '--tags',
                                                       'takes_value': True,
                                                       'value_hint': 'STRING',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_TAGS',
                                                       'description': 'set model tags, '
                                                                      'comma-separated '
                                                                      '(informational, not used '
                                                                      'for routing)'},
                                                   {   'aliases': ['--embd-normalize'],
                                                       'primary': '--embd-normalize',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': ['-1', '0', '1', '2'],
                                                       'default': '2',
                                                       'env': None,
                                                       'description': 'normalisation for '
                                                                      'embeddings (-1=none, 0=max '
                                                                      'absolute int16, 1=taxicab, '
                                                                      '2=euclidean, >2=p-norm)'},
                                                   {   'aliases': ['--host'],
                                                       'primary': '--host',
                                                       'takes_value': True,
                                                       'value_hint': 'HOST',
                                                       'choices': None,
                                                       'default': '127.0.0.1',
                                                       'env': 'LLAMA_ARG_HOST',
                                                       'description': 'ip address to listen, or '
                                                                      'bind to an UNIX socket if '
                                                                      'the address ends with '
                                                                      '.sock'},
                                                   {   'aliases': ['--port'],
                                                       'primary': '--port',
                                                       'takes_value': True,
                                                       'value_hint': 'PORT',
                                                       'choices': None,
                                                       'default': '8080',
                                                       'env': 'LLAMA_ARG_PORT',
                                                       'description': 'port to listen'},
                                                   {   'aliases': ['--reuse-port'],
                                                       'primary': '--reuse-port',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_REUSE_PORT',
                                                       'description': 'allow multiple sockets to '
                                                                      'bind to the same port'},
                                                   {   'aliases': ['--path'],
                                                       'primary': '--path',
                                                       'takes_value': True,
                                                       'value_hint': '<PATH>',
                                                       'choices': None,
                                                       'default': '',
                                                       'env': 'LLAMA_ARG_STATIC_PATH',
                                                       'description': 'path to serve static files '
                                                                      'from'},
                                                   {   'aliases': ['--cors-origins'],
                                                       'primary': '--cors-origins',
                                                       'takes_value': True,
                                                       'value_hint': 'ORIGINS',
                                                       'choices': None,
                                                       'default': '*',
                                                       'env': 'LLAMA_ARG_CORS_ORIGINS',
                                                       'description': 'comma-separated list of '
                                                                      'allowed origins for CORS. '
                                                                      'If set to special value '
                                                                      "'localhost', reflect the "
                                                                      'Origin header only if it is '
                                                                      'localhost.'},
                                                   {   'aliases': ['--cors-methods'],
                                                       'primary': '--cors-methods',
                                                       'takes_value': True,
                                                       'value_hint': 'METHODS',
                                                       'choices': None,
                                                       'default': 'GET, POST, DELETE, OPTIONS',
                                                       'env': 'LLAMA_ARG_CORS_METHODS',
                                                       'description': 'comma-separated list of '
                                                                      'allowed methods for CORS'},
                                                   {   'aliases': ['--cors-headers'],
                                                       'primary': '--cors-headers',
                                                       'takes_value': True,
                                                       'value_hint': 'HEADERS',
                                                       'choices': None,
                                                       'default': '*',
                                                       'env': 'LLAMA_ARG_CORS_HEADERS',
                                                       'description': 'comma-separated list of '
                                                                      'allowed headers for CORS'},
                                                   {   'aliases': [   '--cors-credentials',
                                                                      '--no-cors-credentials'],
                                                       'primary': '--cors-credentials',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled',
                                                       'env': 'LLAMA_ARG_CORS_CREDENTIALS',
                                                       'description': 'whether to allow '
                                                                      'credentials for CORS. Note: '
                                                                      'if this is enabled and '
                                                                      '--cors-origins is set to * '
                                                                      '(default), the Origin '
                                                                      'header will be echoed back, '
                                                                      'and credentials will always '
                                                                      'be allowed.'},
                                                   {   'aliases': ['--api-prefix'],
                                                       'primary': '--api-prefix',
                                                       'takes_value': True,
                                                       'value_hint': '<PREFIX>',
                                                       'choices': None,
                                                       'default': '',
                                                       'env': 'LLAMA_ARG_API_PREFIX',
                                                       'description': 'prefix path the server '
                                                                      'serves from, without the '
                                                                      'trailing slash'},
                                                   {   'aliases': ['--ui-config', '--webui-config'],
                                                       'primary': '--ui-config',
                                                       'takes_value': True,
                                                       'value_hint': 'JSON',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_UI_CONFIG',
                                                       'description': 'JSON that provides default '
                                                                      'UI settings (overrides UI '
                                                                      'defaults)'},
                                                   {   'aliases': [   '--ui-config-file',
                                                                      '--webui-config-file'],
                                                       'primary': '--ui-config-file',
                                                       'takes_value': True,
                                                       'value_hint': 'PATH',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_UI_CONFIG_FILE',
                                                       'description': 'JSON file that provides '
                                                                      'default UI settings '
                                                                      '(overrides UI defaults)'},
                                                   {   'aliases': [   '--ui-mcp-proxy',
                                                                      '--webui-mcp-proxy',
                                                                      '--no-ui-mcp-proxy',
                                                                      '--no-webui-mcp-proxy'],
                                                       'primary': '--ui-mcp-proxy',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_UI_MCP_PROXY',
                                                       'description': 'experimental: whether to '
                                                                      'enable MCP CORS proxy - do '
                                                                      'not enable in untrusted '
                                                                      'environments'},
                                                   {   'aliases': ['--tools'],
                                                       'primary': '--tools',
                                                       'takes_value': True,
                                                       'value_hint': 'TOOL1,TOOL2,...',
                                                       'choices': [   'read_file',
                                                                      'file_glob_search',
                                                                      'grep_search',
                                                                      'exec_shell_command',
                                                                      'write_file',
                                                                      'edit_file',
                                                                      'get_datetime',
                                                                      'get_info',
                                                                      'all'],
                                                       'default': 'no tools',
                                                       'env': 'LLAMA_ARG_TOOLS',
                                                       'description': 'experimental: whether to '
                                                                      'enable built-in tools for '
                                                                      'AI agents - do not enable '
                                                                      'in untrusted environments '
                                                                      '(default: no tools) specify '
                                                                      "'all' to enable all tools "
                                                                      'available tools: read_file, '
                                                                      'file_glob_search, '
                                                                      'grep_search, '
                                                                      'exec_shell_command, '
                                                                      'write_file, edit_file, '
                                                                      'get_datetime, get_info '
                                                                      'note: for security reasons, '
                                                                      'this will limit '
                                                                      '--cors-origins to localhost '
                                                                      'by default'},
                                                   {   'aliases': ['--tools-runtime'],
                                                       'primary': '--tools-runtime',
                                                       'takes_value': True,
                                                       'value_hint': 'OPTION',
                                                       'choices': [   'none',
                                                                      'docker:<image>',
                                                                      'podman:<image>',
                                                                      'docker-container:<id>',
                                                                      'podman-container:<id>',
                                                                      'ssh:<target>'],
                                                       'default': 'none',
                                                       'env': 'LLAMA_ARG_TOOLS_RUNTIME',
                                                       'description': 'experimental: run tools in '
                                                                      'a separate runtime '
                                                                      'environment (default: none, '
                                                                      'use host environment) '
                                                                      'available options: '
                                                                      "'docker:<image>', "
                                                                      "'podman:<image>': spin up a "
                                                                      'new container and reuse it '
                                                                      'for all invocations, clean '
                                                                      'up on server exit '
                                                                      "'docker-container:<id>', "
                                                                      "'podman-container:<id>': "
                                                                      'use an existing container '
                                                                      "by ID, won't stop on server "
                                                                      "exit 'ssh:<target>': run "
                                                                      'tools on a remote POSIX '
                                                                      'host over SSH, key-based '
                                                                      'auth and a trusted host key '
                                                                      'are required'},
                                                   {   'aliases': ['--mcp-servers-config'],
                                                       'primary': '--mcp-servers-config',
                                                       'takes_value': True,
                                                       'value_hint': '<PATH>',
                                                       'choices': None,
                                                       'default': 'none',
                                                       'env': 'LLAMA_ARG_MCP_SERVERS_CONFIG',
                                                       'description': 'experimental: path to JSON '
                                                                      'file with MCP server '
                                                                      'definitions '
                                                                      '(Cursor-compatible format) '
                                                                      '- do not enable in '
                                                                      'untrusted environments '
                                                                      'note: for security reasons, '
                                                                      'this will limit '
                                                                      '--cors-origins to localhost '
                                                                      'by default'},
                                                   {   'aliases': ['--mcp-servers-json'],
                                                       'primary': '--mcp-servers-json',
                                                       'takes_value': True,
                                                       'value_hint': 'JSON',
                                                       'choices': None,
                                                       'default': 'none',
                                                       'env': 'LLAMA_ARG_MCP_SERVERS_JSON',
                                                       'description': 'experimental: inline JSON '
                                                                      'with MCP server definitions '
                                                                      '(Cursor-compatible format) '
                                                                      '- do not enable in '
                                                                      'untrusted environments '
                                                                      'note: for security reasons, '
                                                                      'this will limit '
                                                                      '--cors-origins to localhost '
                                                                      'by default'},
                                                   {   'aliases': [   '-ag',
                                                                      '--agent',
                                                                      '-no-ag',
                                                                      '--no-agent'],
                                                       'primary': '--agent',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_AGENT',
                                                       'description': 'whether to enable CORS '
                                                                      'proxy and all built-in '
                                                                      'tools - do not enable in '
                                                                      'untrusted environments '
                                                                      '(default: disabled) note: '
                                                                      'for security reasons, this '
                                                                      'will limit --cors-origins '
                                                                      'to localhost by default'},
                                                   {   'aliases': [   '--ui',
                                                                      '--webui',
                                                                      '--no-ui',
                                                                      '--no-webui'],
                                                       'primary': '--ui',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_UI',
                                                       'description': 'whether to enable the Web '
                                                                      'UI (default: enabled)'},
                                                   {   'aliases': ['--embedding', '--embeddings'],
                                                       'primary': '--embedding',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_EMBEDDINGS',
                                                       'description': 'restrict to only support '
                                                                      'embedding use case; use '
                                                                      'only with dedicated '
                                                                      'embedding models'},
                                                   {   'aliases': ['--rerank', '--reranking'],
                                                       'primary': '--rerank',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_RERANKING',
                                                       'description': 'enable reranking endpoint '
                                                                      'on server'},
                                                   {   'aliases': [],
                                                       'primary': '--api-key',
                                                       'takes_value': True,
                                                       'value_hint': 'KEY',
                                                       'choices': None,
                                                       'default': 'none',
                                                       'env': 'LLAMA_API_KEY',
                                                       'description': 'API key to use for '
                                                                      'authentication, multiple '
                                                                      'keys can be provided as a '
                                                                      'comma-separated list'},
                                                   {   'aliases': ['--api-key-file'],
                                                       'primary': '--api-key-file',
                                                       'takes_value': True,
                                                       'value_hint': 'FNAME',
                                                       'choices': None,
                                                       'default': 'none',
                                                       'env': 'LLAMA_ARG_API_KEY_FILE',
                                                       'description': 'path to file containing API '
                                                                      'keys, one per line; lines '
                                                                      'starting with a hash are '
                                                                      'treated as comments'},
                                                   {   'aliases': ['--ssl-key-file'],
                                                       'primary': '--ssl-key-file',
                                                       'takes_value': True,
                                                       'value_hint': 'FNAME',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_SSL_KEY_FILE',
                                                       'description': 'path to file a PEM-encoded '
                                                                      'SSL private key'},
                                                   {   'aliases': ['--ssl-cert-file'],
                                                       'primary': '--ssl-cert-file',
                                                       'takes_value': True,
                                                       'value_hint': 'FNAME',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_SSL_CERT_FILE',
                                                       'description': 'path to file a PEM-encoded '
                                                                      'SSL certificate'},
                                                   {   'aliases': ['--chat-template-kwargs'],
                                                       'primary': '--chat-template-kwargs',
                                                       'takes_value': True,
                                                       'value_hint': 'STRING',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_CHAT_TEMPLATE_KWARGS',
                                                       'description': 'sets additional params for '
                                                                      'the json template parser, '
                                                                      'must be a valid json object '
                                                                      'string, e.g. '
                                                                      '\'{"key1":"value1","key2":"value2"}\''},
                                                   {   'aliases': ['-to', '--timeout'],
                                                       'primary': '--timeout',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '3600',
                                                       'env': 'LLAMA_ARG_TIMEOUT',
                                                       'description': 'server read/write timeout '
                                                                      'in seconds'},
                                                   {   'aliases': ['--sse-ping-interval'],
                                                       'primary': '--sse-ping-interval',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '30',
                                                       'env': 'LLAMA_ARG_SSE_PING_INTERVAL',
                                                       'description': 'server SSE ping interval in '
                                                                      'seconds (-1 = disabled, '
                                                                      'default: 30)'},
                                                   {   'aliases': ['--threads-http'],
                                                       'primary': '--threads-http',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '-1',
                                                       'env': 'LLAMA_ARG_THREADS_HTTP',
                                                       'description': 'number of threads used to '
                                                                      'process HTTP requests'},
                                                   {   'aliases': [   '--cache-prompt',
                                                                      '--no-cache-prompt'],
                                                       'primary': '--cache-prompt',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_CACHE_PROMPT',
                                                       'description': 'whether to enable prompt '
                                                                      'caching'},
                                                   {   'aliases': ['--cache-reuse'],
                                                       'primary': '--cache-reuse',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': '0',
                                                       'env': 'LLAMA_ARG_CACHE_REUSE',
                                                       'description': 'min chunk size to attempt '
                                                                      'reusing from the cache via '
                                                                      'KV shifting, requires '
                                                                      'prompt caching to be '
                                                                      'enabled'},
                                                   {   'aliases': ['--metrics'],
                                                       'primary': '--metrics',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_ENDPOINT_METRICS',
                                                       'description': 'enable prometheus '
                                                                      'compatible metrics '
                                                                      'endpoint'},
                                                   {   'aliases': ['--props'],
                                                       'primary': '--props',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_ENDPOINT_PROPS',
                                                       'description': 'enable changing global '
                                                                      'properties via POST /props'},
                                                   {   'aliases': ['--slots', '--no-slots'],
                                                       'primary': '--slots',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled',
                                                       'env': 'LLAMA_ARG_ENDPOINT_SLOTS',
                                                       'description': 'expose slots monitoring '
                                                                      'endpoint'},
                                                   {   'aliases': ['--slot-save-path'],
                                                       'primary': '--slot-save-path',
                                                       'takes_value': True,
                                                       'value_hint': 'PATH',
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': None,
                                                       'description': 'path to save slot kv cache '
                                                                      '(default: disabled)'},
                                                   {   'aliases': ['--media-path'],
                                                       'primary': '--media-path',
                                                       'takes_value': True,
                                                       'value_hint': '<PATH>',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'directory for loading local '
                                                                      'media files; files can be '
                                                                      'accessed via file:// URLs '
                                                                      'using relative paths'},
                                                   {   'aliases': ['--models-dir'],
                                                       'primary': '--models-dir',
                                                       'takes_value': True,
                                                       'value_hint': '<PATH>',
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_MODELS_DIR',
                                                       'description': 'directory containing models '
                                                                      'for the router server'},
                                                   {   'aliases': ['--models-preset'],
                                                       'primary': '--models-preset',
                                                       'takes_value': True,
                                                       'value_hint': 'PATH',
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': 'LLAMA_ARG_MODELS_PRESET',
                                                       'description': 'path to INI file containing '
                                                                      'model presets for the '
                                                                      'router server'},
                                                   {   'aliases': ['--models-max'],
                                                       'primary': '--models-max',
                                                       'takes_value': True,
                                                       'value_hint': 'N',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_MODELS_MAX',
                                                       'description': 'for router server, maximum '
                                                                      'number of models to load '
                                                                      'simultaneously'},
                                                   {   'aliases': [   '--models-autoload',
                                                                      '--no-models-autoload'],
                                                       'primary': '--models-autoload',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_MODELS_AUTOLOAD',
                                                       'description': 'for router server, whether '
                                                                      'to automatically load '
                                                                      'models'},
                                                   {   'aliases': ['--jinja', '--no-jinja'],
                                                       'primary': '--jinja',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'enabled',
                                                       'env': 'LLAMA_ARG_JINJA',
                                                       'description': 'whether to use jinja '
                                                                      'template engine for chat'},
                                                   {   'aliases': ['--reasoning-format'],
                                                       'primary': '--reasoning-format',
                                                       'takes_value': True,
                                                       'value_hint': 'FORMAT',
                                                       'choices': [   'none',
                                                                      'deepseek',
                                                                      'deepseek-legacy'],
                                                       'default': 'auto',
                                                       'env': 'LLAMA_ARG_THINK',
                                                       'description': 'controls whether thought '
                                                                      'tags are allowed and/or '
                                                                      'extracted from the '
                                                                      'response, and in which '
                                                                      "format they're returned; "
                                                                      'one of: none: leaves '
                                                                      'thoughts unparsed in '
                                                                      '`message.content`; '
                                                                      'deepseek: puts thoughts in '
                                                                      '`message.reasoning_content`; '
                                                                      'deepseek-legacy: keeps '
                                                                      '`<think>` tags in '
                                                                      '`message.content` while '
                                                                      'also populating '
                                                                      '`message.reasoning_content`'},
                                                   {   'aliases': ['-rea', '--reasoning'],
                                                       'primary': '--reasoning',
                                                       'takes_value': True,
                                                       'value_hint': '<on|off|auto>',
                                                       'choices': ['on', 'off', 'auto'],
                                                       'default': 'auto',
                                                       'env': 'LLAMA_ARG_REASONING',
                                                       'description': 'Use reasoning/thinking in '
                                                                      "the chat ('on', 'off', or "
                                                                      "'auto', default: 'auto' "
                                                                      '(detect from template))'},
                                                   {   'aliases': ['--unknown'],
                                                       'primary': '--unknown',
                                                       'takes_value': False,
                                                       'value_hint': '--reasoning-budget N',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'token budget for thinking: '
                                                                      '-1 for unrestricted, 0 for '
                                                                      'immediate end,\n'
                                                                      'N>0 for token budget '
                                                                      '(default: -1)\n'
                                                                      '(env: '
                                                                      'LLAMA_ARG_THINK_BUDGET)'},
                                                   {   'aliases': ['--reasoning-budget-message'],
                                                       'primary': '--reasoning-budget-message',
                                                       'takes_value': True,
                                                       'value_hint': 'MESSAGE',
                                                       'choices': None,
                                                       'default': 'none',
                                                       'env': 'LLAMA_ARG_THINK_BUDGET_MESSAGE',
                                                       'description': 'message injected before the '
                                                                      'end-of-thinking tag when '
                                                                      'reasoning budget is '
                                                                      'exhausted'},
                                                   {   'aliases': [   '--reasoning-preserve',
                                                                      '--no-reasoning-preserve'],
                                                       'primary': '--reasoning-preserve',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_REASONING_PRESERVE',
                                                       'description': 'preserve reasoning trace in '
                                                                      'the full history, not just '
                                                                      'the last assistant message '
                                                                      'compatible with certain '
                                                                      'templates having '
                                                                      "'supports_preserve_reasoning' "
                                                                      'capability example: '
                                                                      'https://docs.z.ai/guides/capabilities/thinking-mode#preserved-thinking'},
                                                   {   'aliases': ['--chat-template'],
                                                       'primary': '--chat-template',
                                                       'takes_value': True,
                                                       'value_hint': 'JINJA_TEMPLATE',
                                                       'choices': [   'bailing',
                                                                      'bailing-think',
                                                                      'bailing2',
                                                                      'chatglm3',
                                                                      'chatglm4',
                                                                      'chatml',
                                                                      'command-r',
                                                                      'deepseek',
                                                                      'deepseek-ocr',
                                                                      'deepseek2',
                                                                      'deepseek3',
                                                                      'exaone-moe',
                                                                      'exaone3',
                                                                      'exaone4',
                                                                      'falcon3',
                                                                      'gemma',
                                                                      'gigachat',
                                                                      'glmedge',
                                                                      'gpt-oss',
                                                                      'granite',
                                                                      'granite-4.0',
                                                                      'granite-4.1',
                                                                      'grok-2',
                                                                      'hunyuan-dense',
                                                                      'hunyuan-moe',
                                                                      'hunyuan-vl',
                                                                      'kimi-k2',
                                                                      'llama2',
                                                                      'llama2-sys',
                                                                      'llama2-sys-bos',
                                                                      'llama2-sys-strip',
                                                                      'llama3',
                                                                      'llama4',
                                                                      'megrez',
                                                                      'minicpm',
                                                                      'mistral-v1',
                                                                      'mistral-v3',
                                                                      'mistral-v3-tekken',
                                                                      'mistral-v7',
                                                                      'mistral-v7-tekken',
                                                                      'monarch',
                                                                      'openchat',
                                                                      'orion',
                                                                      'pangu-embedded',
                                                                      'phi3',
                                                                      'phi4',
                                                                      'rwkv-world',
                                                                      'seed_oss',
                                                                      'smolvlm',
                                                                      'solar-open',
                                                                      'vicuna',
                                                                      'vicuna-orca',
                                                                      'yandex',
                                                                      'zephyr'],
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_CHAT_TEMPLATE',
                                                       'description': 'set custom jinja chat '
                                                                      'template (default: template '
                                                                      "taken from model's "
                                                                      'metadata) if suffix/prefix '
                                                                      'are specified, template '
                                                                      'will be disabled only '
                                                                      'commonly used templates are '
                                                                      'accepted (unless --jinja is '
                                                                      'set before this flag): list '
                                                                      'of built-in templates: '
                                                                      'bailing, bailing-think, '
                                                                      'bailing2, chatglm3, '
                                                                      'chatglm4, chatml, '
                                                                      'command-r, deepseek, '
                                                                      'deepseek-ocr, deepseek2, '
                                                                      'deepseek3, exaone-moe, '
                                                                      'exaone3, exaone4, falcon3, '
                                                                      'gemma, gigachat, glmedge, '
                                                                      'gpt-oss, granite, '
                                                                      'granite-4.0, granite-4.1, '
                                                                      'grok-2, hunyuan-dense, '
                                                                      'hunyuan-moe, hunyuan-vl, '
                                                                      'kimi-k2, llama2, '
                                                                      'llama2-sys, llama2-sys-bos, '
                                                                      'llama2-sys-strip, llama3, '
                                                                      'llama4, megrez, minicpm, '
                                                                      'mistral-v1, mistral-v3, '
                                                                      'mistral-v3-tekken, '
                                                                      'mistral-v7, '
                                                                      'mistral-v7-tekken, monarch, '
                                                                      'openchat, orion, '
                                                                      'pangu-embedded, phi3, phi4, '
                                                                      'rwkv-world, seed_oss, '
                                                                      'smolvlm, solar-open, '
                                                                      'vicuna, vicuna-orca, '
                                                                      'yandex, zephyr'},
                                                   {   'aliases': ['--chat-template-file'],
                                                       'primary': '--chat-template-file',
                                                       'takes_value': True,
                                                       'value_hint': 'JINJA_TEMPLATE_FILE',
                                                       'choices': [   'bailing',
                                                                      'bailing-think',
                                                                      'bailing2',
                                                                      'chatglm3',
                                                                      'chatglm4',
                                                                      'chatml',
                                                                      'command-r',
                                                                      'deepseek',
                                                                      'deepseek-ocr',
                                                                      'deepseek2',
                                                                      'deepseek3',
                                                                      'exaone-moe',
                                                                      'exaone3',
                                                                      'exaone4',
                                                                      'falcon3',
                                                                      'gemma',
                                                                      'gigachat',
                                                                      'glmedge',
                                                                      'gpt-oss',
                                                                      'granite',
                                                                      'granite-4.0',
                                                                      'granite-4.1',
                                                                      'grok-2',
                                                                      'hunyuan-dense',
                                                                      'hunyuan-moe',
                                                                      'hunyuan-vl',
                                                                      'kimi-k2',
                                                                      'llama2',
                                                                      'llama2-sys',
                                                                      'llama2-sys-bos',
                                                                      'llama2-sys-strip',
                                                                      'llama3',
                                                                      'llama4',
                                                                      'megrez',
                                                                      'minicpm',
                                                                      'mistral-v1',
                                                                      'mistral-v3',
                                                                      'mistral-v3-tekken',
                                                                      'mistral-v7',
                                                                      'mistral-v7-tekken',
                                                                      'monarch',
                                                                      'openchat',
                                                                      'orion',
                                                                      'pangu-embedded',
                                                                      'phi3',
                                                                      'phi4',
                                                                      'rwkv-world',
                                                                      'seed_oss',
                                                                      'smolvlm',
                                                                      'solar-open',
                                                                      'vicuna',
                                                                      'vicuna-orca',
                                                                      'yandex',
                                                                      'zephyr'],
                                                       'default': "template taken from model's "
                                                                  'metadata',
                                                       'env': 'LLAMA_ARG_CHAT_TEMPLATE_FILE',
                                                       'description': 'set custom jinja chat '
                                                                      'template file (default: '
                                                                      "template taken from model's "
                                                                      'metadata) if suffix/prefix '
                                                                      'are specified, template '
                                                                      'will be disabled only '
                                                                      'commonly used templates are '
                                                                      'accepted (unless --jinja is '
                                                                      'set before this flag): list '
                                                                      'of built-in templates: '
                                                                      'bailing, bailing-think, '
                                                                      'bailing2, chatglm3, '
                                                                      'chatglm4, chatml, '
                                                                      'command-r, deepseek, '
                                                                      'deepseek-ocr, deepseek2, '
                                                                      'deepseek3, exaone-moe, '
                                                                      'exaone3, exaone4, falcon3, '
                                                                      'gemma, gigachat, glmedge, '
                                                                      'gpt-oss, granite, '
                                                                      'granite-4.0, granite-4.1, '
                                                                      'grok-2, hunyuan-dense, '
                                                                      'hunyuan-moe, hunyuan-vl, '
                                                                      'kimi-k2, llama2, '
                                                                      'llama2-sys, llama2-sys-bos, '
                                                                      'llama2-sys-strip, llama3, '
                                                                      'llama4, megrez, minicpm, '
                                                                      'mistral-v1, mistral-v3, '
                                                                      'mistral-v3-tekken, '
                                                                      'mistral-v7, '
                                                                      'mistral-v7-tekken, monarch, '
                                                                      'openchat, orion, '
                                                                      'pangu-embedded, phi3, phi4, '
                                                                      'rwkv-world, seed_oss, '
                                                                      'smolvlm, solar-open, '
                                                                      'vicuna, vicuna-orca, '
                                                                      'yandex, zephyr'},
                                                   {   'aliases': [   '--skip-chat-parsing',
                                                                      '--no-skip-chat-parsing'],
                                                       'primary': '--skip-chat-parsing',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_SKIP_CHAT_PARSING',
                                                       'description': 'force a pure content '
                                                                      'parser, even if a Jinja '
                                                                      'template is specified; '
                                                                      'model will output '
                                                                      'everything in the content '
                                                                      'section, including any '
                                                                      'reasoning and/or tool '
                                                                      'calls'},
                                                   {   'aliases': [   '--prefill-assistant',
                                                                      '--no-prefill-assistant'],
                                                       'primary': '--prefill-assistant',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': 'LLAMA_ARG_PREFILL_ASSISTANT',
                                                       'description': 'whether to prefill the '
                                                                      "assistant's response if the "
                                                                      'last message is an '
                                                                      'assistant message (default: '
                                                                      'prefill enabled) when this '
                                                                      'flag is set, if the last '
                                                                      'message is an assistant '
                                                                      'message then it will be '
                                                                      'treated as a full message '
                                                                      'and not prefilled'},
                                                   {   'aliases': [   '-sps',
                                                                      '--slot-prompt-similarity'],
                                                       'primary': '--slot-prompt-similarity',
                                                       'takes_value': True,
                                                       'value_hint': 'SIMILARITY',
                                                       'choices': None,
                                                       'default': '0.10',
                                                       'env': None,
                                                       'description': 'how much the prompt of a '
                                                                      'request must match the '
                                                                      'prompt of a slot in order '
                                                                      'to use that slot (0.0 = '
                                                                      'disabled)'},
                                                   {   'aliases': ['--lora-init-without-apply'],
                                                       'primary': '--lora-init-without-apply',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': None,
                                                       'description': 'load LoRA adapters without '
                                                                      'applying them (apply later '
                                                                      'via POST /lora-adapters)'},
                                                   {   'aliases': ['--sleep-idle-seconds'],
                                                       'primary': '--sleep-idle-seconds',
                                                       'takes_value': True,
                                                       'value_hint': 'SECONDS',
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'number of seconds of '
                                                                      'idleness after which the '
                                                                      'server will sleep'},
                                                   {   'aliases': ['--log-prompts-dir'],
                                                       'primary': '--log-prompts-dir',
                                                       'takes_value': True,
                                                       'value_hint': '<PATH>',
                                                       'choices': None,
                                                       'default': 'disabled',
                                                       'env': None,
                                                       'description': 'Log prompts to directory '
                                                                      '(auto-created if not '
                                                                      'present; only used for '
                                                                      'debugging)'},
                                                   {   'aliases': ['--embd-gemma-default'],
                                                       'primary': '--embd-gemma-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use default EmbeddingGemma '
                                                                      'model (note: can download '
                                                                      'weights from the internet)'},
                                                   {   'aliases': ['--fim-qwen-1.5b-default'],
                                                       'primary': '--fim-qwen-1.5b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use default Qwen 2.5 Coder '
                                                                      '1.5B (note: can download '
                                                                      'weights from the internet)'},
                                                   {   'aliases': ['--fim-qwen-3b-default'],
                                                       'primary': '--fim-qwen-3b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use default Qwen 2.5 Coder '
                                                                      '3B (note: can download '
                                                                      'weights from the internet)'},
                                                   {   'aliases': ['--fim-qwen-7b-default'],
                                                       'primary': '--fim-qwen-7b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use default Qwen 2.5 Coder '
                                                                      '7B (note: can download '
                                                                      'weights from the internet)'},
                                                   {   'aliases': ['--fim-qwen-7b-spec'],
                                                       'primary': '--fim-qwen-7b-spec',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use Qwen 2.5 Coder 7B + '
                                                                      '0.5B draft for speculative '
                                                                      'decoding (note: can '
                                                                      'download weights from the '
                                                                      'internet)'},
                                                   {   'aliases': ['--fim-qwen-14b-spec'],
                                                       'primary': '--fim-qwen-14b-spec',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use Qwen 2.5 Coder 14B + '
                                                                      '0.5B draft for speculative '
                                                                      'decoding (note: can '
                                                                      'download weights from the '
                                                                      'internet)'},
                                                   {   'aliases': ['--fim-qwen-30b-default'],
                                                       'primary': '--fim-qwen-30b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use default Qwen 3 Coder '
                                                                      '30B A3B Instruct (note: can '
                                                                      'download weights from the '
                                                                      'internet)'},
                                                   {   'aliases': ['--gpt-oss-20b-default'],
                                                       'primary': '--gpt-oss-20b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use gpt-oss-20b (note: can '
                                                                      'download weights from the '
                                                                      'internet)'},
                                                   {   'aliases': ['--gpt-oss-120b-default'],
                                                       'primary': '--gpt-oss-120b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use gpt-oss-120b (note: can '
                                                                      'download weights from the '
                                                                      'internet)'},
                                                   {   'aliases': ['--vision-gemma-4b-default'],
                                                       'primary': '--vision-gemma-4b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use Gemma 3 4B QAT (note: '
                                                                      'can download weights from '
                                                                      'the internet)'},
                                                   {   'aliases': ['--vision-gemma-12b-default'],
                                                       'primary': '--vision-gemma-12b-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'use Gemma 3 12B QAT (note: '
                                                                      'can download weights from '
                                                                      'the internet)'},
                                                   {   'aliases': ['--spec-default'],
                                                       'primary': '--spec-default',
                                                       'takes_value': False,
                                                       'value_hint': None,
                                                       'choices': None,
                                                       'default': None,
                                                       'env': None,
                                                       'description': 'enable default speculative '
                                                                      'decoding config'}]}}
