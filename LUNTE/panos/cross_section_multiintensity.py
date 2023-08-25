# Import Necessary Libraries

import numpy as np
import matplotlib.pyplot as plt
import os

# get a list of all CSV files in the data folder
csv_files = [f for f in os.listdir(".") if f.endswith('.csv')]

# loop over each CSV file in the folder and generate a cross-section plot
for csv_file in csv_files:

        data = np.loadtxt(open(csv_file, "rb"), delimiter=";")	#, skiprows=1)	# read data from the CSV file

        # convert ADC laser intensity values to pulse energies in pJ
        # This conversion is at 10 ns pulse width for DLTM 2
        data = 4E-12*data**4 - 1E-07*data**3 + 0.0004*data**2+0.139*data-146.13
        print (data)

        pulse_energies, occurrence_count = np.unique(data, return_counts=True)	#gets unique elements & their occurrence counts from data
        print(f"pulse_energies: {pulse_energies}")
        print(f"occurrence_count: {occurrence_count}")
        numberOfValues = pulse_energies.shape[0]#-1 # -1 = ignore last value (=value for no-SEL)
        rows, cols = data.shape
        pixels=rows*cols
        cross_section = []	# list for cross-section-curve values
        SELcount = 0	# buffer for cross-section-value-integrator

        for value in range(1,numberOfValues):	#go through all values of PulseEnergies
                SELcount+=occurrence_count[value]	#add to SEL-integrator
                cross_section.append(SELcount/pixels)	#write into result-curve and set relative to scan size	

        pulse_energies = pulse_energies[1:numberOfValues]	#remove last value to get same size (->cross_section)
        print(f"num_latchups: {SELcount}	pixels: {pixels}	file: {csv_file}")
        #	print(f"cross_section: {cross_section}")

        #	x_step, y_step = 0.25, 0.25  # in micrometers
        pixel_area = 1	#x_step * y_step  # set pixel area in square micrometers
        #	effective_area = cols * rows * pixel_area	# calculate size of scanned area

        # Uncomment this to limit the number of data points to 100 if there are many data points in graph
        #	pulse_energies = pulse_energies[::int(len(pulse_energies)/100)]
        #	cross_section = cross_section[::int(len(cross_section)/100)]

        # plot the data
        fig1, ax1 = plt.subplots(figsize=(6, 4), dpi=200)



        ##	ax1.scatter(pulse_energies , cross_section, s=5, rasterized=True) #s=datapoint-size
        #plot csv data
        ax1.scatter(pulse_energies , cross_section, color = 'blue', label = 'extracted from corrected picture', s=5, rasterized=True)	
        print(cross_section)
        
        #plot SEL/ION Data
        cs = np.array([0.0210415175686719])
        ax1.scatter(pulse_energies , cs, color = 'red', label = 'calculated (SEL/ION)', s=5, rasterized=True)

        #plot uncorrected Data
        #plot SEL/ION Data
        cs = np.array([0.024967159014450034])
        ax1.scatter(pulse_energies , cs, color = 'green', label = 'extracted from uncorrected picture', s=5, rasterized=True)

        # set axis labels and title
        ax1.set_xlabel('Pulse Energy [pJ]', fontsize=12)
        ax1.set_ylabel('SEL X-section [mm²]', fontsize=12)
        ax1.set_title(f'Latchup Cross Section vs Pulse Energy ({csv_file})', fontsize=12)
        ax1.grid(color='gray', linestyle='--', linewidth=0.5)
        ax1.tick_params(axis='both', which='major', labelsize=10)
        ax1.set_yscale('log')	#logarithmic y-scale
        ax1.legend()
        plt.show()	#show the diagram
        fig1.savefig(f"{csv_file}.svg")	#save diagram as svg-file
        fig1.savefig(f"{csv_file}.png")	#save diagram as png-file
        #	np.savetxt('np.csv', pulse_energies cross_section, delimiter=';', header='pulse energy, cross-section')	# , fmt='%.2f'
	
