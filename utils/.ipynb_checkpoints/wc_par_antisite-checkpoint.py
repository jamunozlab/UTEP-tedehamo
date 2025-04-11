import numpy as np
from ovito.io import import_file
import WarrenCowleyParameters as wc

# def wc_params(input_files_dict, nneigh, slice_size):
#     nn = len(nneigh) - 1

#     NiTi_params = {}
#     NiNi_params = {}
#     TiNi_params = {}
#     TiTi_params = {}

#     def average_slices(params_dict, slice_size):
#         averaged_params = {}
#         for concentration, arrays in params_dict.items():
#             num_slices = len(arrays) // slice_size
#             averaged_arrays = []

#             for i in range(num_slices):
#                 slice_arrays = arrays[i * slice_size:(i + 1) * slice_size]
#                 slice_avg = np.mean(slice_arrays, axis=0)
#                 averaged_arrays.append(slice_avg.tolist())

#             averaged_params[concentration] = averaged_arrays
#         return averaged_params

#     for concentration, files in input_files_dict.items():
#         NiTi_params[concentration] = []
#         NiNi_params[concentration] = []
#         TiNi_params[concentration] = []
#         TiTi_params[concentration] = []

#         for file in files:
#             pipeline = import_file(file)
#             mod = wc.WarrenCowleyParameters(nneigh=nneigh, only_selected=False)
#             pipeline.modifiers.append(mod)
#             data = pipeline.compute()
#             wc_for_shells = data.attributes["Warren-Cowley parameters"]

#             NiTi = [np.round(wc_for_shells[i, 0][0], 4) for i in range(nn)]
#             NiNi = [np.round(wc_for_shells[i, 1][1], 4) for i in range(nn)]
#             TiNi = [np.round(wc_for_shells[i, 0][0], 4) for i in range(nn)]
#             TiTi = [np.round(wc_for_shells[i, 1][1], 4) for i in range(nn)]

#             NiTi_params[concentration].append(NiTi)
#             NiNi_params[concentration].append(NiNi)
#             TiNi_params[concentration].append(TiNi)
#             TiTi_params[concentration].append(TiTi)

#     NiTi_averaged = average_slices(NiTi_params, slice_size)
#     NiNi_averaged = average_slices(NiNi_params, slice_size)
#     TiNi_averaged = average_slices(TiNi_params, slice_size)
#     TiTi_averaged = average_slices(TiTi_params, slice_size)

#     return NiTi_averaged, NiNi_averaged, TiNi_averaged, TiTi_averaged

def wc_params(input_files_dict, nneigh, slice_size):
    nn = len(nneigh) - 1

    NiTi_params = {}
    NiNi_params = {}
    TiNi_params = {}
    TiTi_params = {}

    def average_slices(params_dict, slice_size):
        averaged_params = {}
        errors_params = {}
        
        for concentration, arrays in params_dict.items():
            num_slices = len(arrays) // slice_size
            averaged_arrays = []
            error_arrays = []

            for i in range(num_slices):
                slice_arrays = arrays[i * slice_size:(i + 1) * slice_size]
                slice_avg = np.mean(slice_arrays, axis=0)
                slice_std = np.std(slice_arrays, axis=0)

                averaged_arrays.append(slice_avg.tolist())
                error_arrays.append(slice_std.tolist())

            averaged_params[concentration] = averaged_arrays
            errors_params[concentration] = error_arrays

        return averaged_params, errors_params

    for concentration, files in input_files_dict.items():
        NiTi_params[concentration] = []
        NiNi_params[concentration] = []
        TiNi_params[concentration] = []
        TiTi_params[concentration] = []

        for file in files:
            pipeline = import_file(file)
            mod = wc.WarrenCowleyParameters(nneigh=nneigh, only_selected=False)
            pipeline.modifiers.append(mod)
            data = pipeline.compute()
            wc_for_shells = data.attributes["Warren-Cowley parameters"]

            NiTi = [np.round(wc_for_shells[i, 0][0], 4) for i in range(nn)]
            NiNi = [np.round(wc_for_shells[i, 1][1], 4) for i in range(nn)]
            TiNi = [np.round(wc_for_shells[i, 0][0], 4) for i in range(nn)]
            TiTi = [np.round(wc_for_shells[i, 1][1], 4) for i in range(nn)]

            NiTi_params[concentration].append(NiTi)
            NiNi_params[concentration].append(NiNi)
            TiNi_params[concentration].append(TiNi)
            TiTi_params[concentration].append(TiTi)

    NiTi_averaged, NiTi_errors = average_slices(NiTi_params, slice_size)
    NiNi_averaged, NiNi_errors = average_slices(NiNi_params, slice_size)
    TiNi_averaged, TiNi_errors = average_slices(TiNi_params, slice_size)
    TiTi_averaged, TiTi_errors = average_slices(TiTi_params, slice_size)

    return (NiTi_averaged, NiTi_errors,
            NiNi_averaged, NiNi_errors,
            TiNi_averaged, TiNi_errors,
            TiTi_averaged, TiTi_errors)
