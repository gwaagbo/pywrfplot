pywrfplot itself isn't really installed since you need to work with the code. So just download/copy all the source files to some folder on your computer and run [example.py](http://code.google.com/p/pywrfplot/source/browse/trunk/example.py).

However, the dependencies must be available in your Python runtime environment:
  * [Python 2.x](http://www.python.org/)
  * [NumPy](http://numpy.scipy.org/)
  * [Matplotlib](http://matplotlib.github.com)
  * [Basemap](http://matplotlib.github.com/basemap/)
  * [NetCDF4](http://code.google.com/p/netcdf4-python/)


**Windows:** Install [Python(x,y)](http://code.google.com/p/pythonxy/) first - this is a great Python distribution for Windows that includes a lot of useful features. If I remember correctly you may have to install [Basemap](http://sourceforge.net/projects/matplotlib/files/matplotlib-toolkits/) in addition, look for the Windows installation file.

**Linux:** Python is usually distributed with Linux, and most of the dependecies are easy to install in addition. However, I'm still struggling with Basemap. Will update when I've figured out how to do it.

In addition, the code assumes that you have added
  * `C:\Python27\Lib\site-packages\matplotlib` and
  * `C:\Python27\Lib\site-packages\mpl_toolkits`
to your PYTHONPATH (of course, these must be adjusted to your installation).