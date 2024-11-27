from Mode import Mode
import math
import numpy as np
class UniformMode(Mode):
    
    def __init__(self, sliders_widget,sample_instance, graph2,graph3, graph1, spectrogram_widget2,  num_of_sliders: int=10):
        super().__init__(sliders_widget, num_of_sliders, sample_instance,graph2,graph3, spectrogram_widget2, graph1)
        self.freq_ranges = [[] for i in range (10)]
        self.sliders_values_array= np.ones(10)
        self.attenuation_array= None
    
    def init_mode(self):
        # Sort frequencies and determine ranges
        freq_list= self.sample.frequencies
        min_freq, max_freq = freq_list[0], freq_list[-1]
        total_range = max_freq - min_freq
        step_size = total_range / len(self.sliders_list)
        # Assign frequencies to corresponding ranges
        for i in range(10): 
            range_start = int(min_freq + i * step_size)
            range_end = int(range_start + step_size)
            for comp in freq_list:
                if range_start <= comp <= range_end:
                    self.freq_ranges[i].append(comp)
                elif comp > range_end:
                     continue
        
        #print(f"Uniform freq range:{self.freq_ranges}")
    

    def update_mode_upon_sliders_change(self, slider_index, gain_value, freq_list, freq_mag, freq_phase):
        
        self.attenuation_array= np.ones(len(freq_mag))

        for slider_num,slider in enumerate(self.sliders_list):
            self.sliders_values_array[slider_num]=(slider.value()/5)

        # Apply gain only to frequencies within the specified range
        for i, freq_range in enumerate (self.freq_ranges):
            self.attenuation_array = np.where((freq_list >= freq_range[0]) & (freq_list <= freq_range[1]),
                                    self.attenuation_array * self.sliders_values_array[i], 
                                    self.attenuation_array)
        
        freq_mag= np.array(freq_mag)
        new_freq_magnitude= (freq_mag*self.attenuation_array).tolist()
        
        print(new_freq_magnitude[0]/freq_mag[0])

        # Plot the updated frequency domain
        self.plot_fourier_domain(freq_list, new_freq_magnitude)
        self.plot_inverse_fourier(new_freq_magnitude, freq_phase, self.time, self.graph2)
 
