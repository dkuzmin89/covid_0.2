import pandas as pd

url_conf = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv'
url_d = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv'
url_r = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv'
conf_all = pd.read_csv(url_conf)
d_all = pd.read_csv(url_d)
r_all = pd.read_csv(url_r)


# columns_preparation
def cols_prep(source):
    data_col = source.columns
    data_col = list(data_col)
    cols = data_col[4:]
    return cols


# values_preparation
def val_prep(source, country):
    df = source
    inp = df.loc[df['Country/Region'] == country]
    inp = inp.iloc[0:, 4:]
    vals = inp.values.tolist()
    vals = vals[0]
    return vals


if __name__ == '__main__':

    print('Do you want to observe ONE country or COMPARE two?')
    inp = input()
    inp = inp.lower()

    if inp == 'one':
        print('Enter the name of Country:')
        country = input()
        try:
            country = country.lower().title()
            data = {'Period': cols_prep(conf_all),
                    'New_cases': val_prep(conf_all, country),
                    'Deaths': val_prep(d_all, country),
                    'Recovered': val_prep(r_all, country)}
            out = pd.DataFrame(data)

            # !!! ONY for ITALY correction for 12/03/20
            if country == 'Italy':
                out.iloc[50, 1:] = [15133, 1016, 1045]

            out.to_csv("/Users/dmitry/python_projects/tableau/data/_covid_{0:s}.csv".format(country), index=False)
            print('Your files saved as _covid_{0:s}.csv'.format(country))
        except IndexError:
            print('No such country!')


    elif inp == "compare":
        print('Enter first country:')
        country_1 = input()
        country_1 = country_1.lower().title()
        print('Enter second country:')
        country_2 = input()
        country_2 = country_2.lower().title()

        try:
            data_1 = {'Country': country_1,
                      'Period': cols_prep(conf_all),
                      'New_cases': val_prep(conf_all, country_1),
                      'Deaths': val_prep(d_all, country_1),
                      'Recovered': val_prep(r_all, country_1)}
            data_2 = {'Country': country_2,
                      'Period': cols_prep(conf_all),
                      'New_cases': val_prep(conf_all, country_2),
                      'Deaths': val_prep(d_all, country_2),
                      'Recovered': val_prep(r_all, country_2)}

            out_1 = pd.DataFrame(data_1)
            out_2 = pd.DataFrame(data_2)

            out_1 = out_1.set_index(['Country', 'Period'])
            out_2 = out_2.set_index(['Country', 'Period'])

            out_f = out_1.append(out_2)

            out_f.to_csv(
                "/Users/dmitry/python_projects/tableau/data/_covid_{0:s}+{1:s}.csv".format(country_1, country_2))
            print('Your files saved as _covid_{0:s}+{1:s}.csv"'.format(country_1, country_2))
        except IndexError:
            print("You've made an error in one of the countries")

    else:
        print('Next time enter only "one" or "compare"')
