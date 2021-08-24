import matplotlib.pyplot as plt
import tephi

if __name__ == '__main__':
    import matplotlib.pyplot as plt
    import os.path
    from matplotlib.ticker import FixedLocator

    import tephi

    dew_point = os.path.join(tephi.DATA_DIR, 'dews.txt')
    dew_data = tephi.loadtxt(dew_point, column_titles=('pressure', 'dewpoint'))
    dews = zip(dew_data.pressure, dew_data.dewpoint)
    tpg = tephi.Tephigram(anchor=[(1000, 0), (300, 0)], isotherm_locator=1, dry_adiabat_locator=1)
    tpg.plot(dews)
    plt.show()
