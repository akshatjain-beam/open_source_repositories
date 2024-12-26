from matplotlib import pyplot as plt


def plot_with_uncertainty(df, key=None, **kwargs):
    """
    Plots data from a DataFrame with optional uncertainty represented by error bars.

    This function checks if a `key` is provided. If it is, the function retrieves the left and 
    right standard deviation columns corresponding to the key and plots the data with error bars 
    representing the uncertainty. The standard deviation columns should be named as follows:
    - '{key}_std_dev_left' for the left uncertainty.
    - '{key}_std_dev_right' for the right uncertainty.

    If `key` is not provided, the function checks if the DataFrame has a 'nominal_value' attribute. 
    If it does, it plots the 'nominal_value' with its associated standard deviation as error bars. 
    If neither condition is met, it simply plots the DataFrame without error bars.

    Parameters:
    df : pandas.DataFrame
        The DataFrame containing the data to be plotted. It should include:
        - A column corresponding to the specified key (if `key` is provided).
        - Standard deviation columns named '{key}_std_dev_left' and '{key}_std_dev_right' 
          for uncertainty representation.
        - A 'nominal_value' column (if applicable) for plotting when `key` is None.

    key : str, optional
        The column name in the DataFrame to be plotted. This key is used to determine the data 
        to be visualized and its associated uncertainties. If None, the function will attempt to 
        plot the 'nominal_value' if it exists. Defaults to None

    **kwargs : keyword arguments
        Additional keyword arguments passed to the plotting function.

    Returns:
    matplotlib.artist.Artist
        The artist object representing the plotted data when `key` is provided. If `key` is None,
        the function will plot directly without returning any value.

    """
    $PlaceHolder$
