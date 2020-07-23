import pandas as pd
import geopandas
import matplotlib.pyplot as plt
import argparse


def plot_map(open_cities, closed_cities, filepath='../geo.csv'):
    df = pd.read_csv('geo.csv')
    df_open = df[df['City'].isin(open_cities)]
    df_closed = df[df['City'].isin(closed_cities)]

    gdf_open = geopandas.GeoDataFrame(
        df_open, geometry=geopandas.points_from_xy(df_open.Longitude, df_open.Latitude))
    gdf_closed = geopandas.GeoDataFrame(
        df_closed, geometry=geopandas.points_from_xy(df_closed.Longitude, df_closed.Latitude))

    world = geopandas.read_file(
        geopandas.datasets.get_path('naturalearth_lowres'))

    # We restrict to South America.
    ax = world[world.name == 'United States of America'].plot(
        color='white', edgecolor='black')

    # We can now plot our ``GeoDataFrame``
    gdf_open.plot(ax=ax, color='blue')
    gdf_closed.plot(ax=ax, color='gray')

    ax.set_xlim(xmin=-130, xmax=-65)
    ax.set_ylim(ymin=20, ymax=55)
    ax.set_yticks([])
    ax.set_xticks([])
    ax.set_aspect(1.2)

    ax.legend(['Open cites', 'Closed cities'])

    plt.show()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--csv-path')
    args = parser.parse_args()
    plot_map(args.csv_path)


if __name__ == '__main__':
    main()
