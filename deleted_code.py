    '''                                                                                                   
    # create function                                                                                     
    t = np.arange(0.1, 10.0, 0.1) # x-axis                                                                
    s = np.log10(t) # y-axis                                                                              
    curve = np.polyfit(s, s, 1)                                                                           
    print(curve)                                                                                          
    exit()                                                                                                
    fig,ax = plt.subplots()                                                                               
    ax.plot(t,s)                                                                                          
    ax.grid(True)                                                                                         
    plt.show()                                                                                            
    exit()                                                                                                
                                                                                                          
    np.random.seed(19680801)                                                                              
    mu = 200; sigma = 25; n_bins = 50                                                                     
    x = np.random.normal(mu, sigma, size=100)                                                             
    fig,ax = plt.subplots()                                                                               
    n, bins, patches = ax.hist(x, n_bins)                                                                 
    y = ( (1 / (np.sqrt(2 * np.pi) * sigma)) * np.exp(-0.5 * (1 / sigma * (bins - mu)) ** 2 ))            
    y = y.cumsum()                                                                                        
    y /= y[-1]                                                                                            
    ax.plot(bins, y, 'k--', linewidth=1.5, label='Theoretical')                                           
    plt.show()                                                                                            
    exit()                                                                                                
    '''


    '''                                                                                                   
    log = np.log(vc.loc[:, "Depth (m)"])                                                                  
    curve = np.polyfit(log, vc.loc[:, "Damage (£)"], 1)                                                   
    a = curve[0]; b = curve[1]                                                                            
    s = a * np.log10(vc.loc[:, "Depth (m)"]) + b                                                          
    '''

    # create DataFrame to hold vulnerability curve data for quick plotting                      
    vc = pd.DataFrame(
        {
            "Depth (m)": (0.0001, 0.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5,
                          7.5, 8.5, 9.5),
            "Damage (£)": (0, 50000, 80000, 95000, 105000, 112500, 120000,
                           125000, 130000, 132500, 134000),
            }
        )

        md = max_damage
        vc = pd.DataFrame(
            {"Depth (m)": (0.00001, 0.001, 1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 7.0, 8.0, 9.0, 10.0),
             "Damage (£)": (0, md*0.37, md*0.60, md*0.71, md*0.78, md*0.84, md*0.90,
                               md*0.93, md*0.96, md*0.99, md),}
            )

    min_value = df['Depth (m)'].min()
    max_value = df['Depth (m)'].max()

    # produce plot (troubleshooting)
    fig, ax = plt.subplots()
    ax.plot(vc.loc[:, "Depth (m)"],func)
    plt.show()
    exit()

    popt,pcov = curve_fit(log_func, vc.loc[:, "Depth (m)"], vc.loc[:, "Damage (£)"])
    a = popt[0]; b = popt[1]
    print("a = ",popt[0])
    print("b = ",popt[1])
    s = a + b*np.log10(vc.loc[:, "Depth (m)"])

    fig,ax = plt.subplots()
    ax.plot(vc.loc[:, "Depth (m)"],s)
    ax.grid(True)
    plt.show()
    exit()

    ax.set(xlabel='Inundation depth (m)', ylabel='Damage (£)',
           title='Inundation depth-damage function (vulnerability curve)')
    ax.grid()
    plt.show()
    exit()
