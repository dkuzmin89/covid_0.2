import pandas as pd

pd.set_option('mode.chained_assignment', None)

url_conf = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url_d = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv'
conf_all = pd.read_csv(url_conf)
d_all = pd.read_csv(url_d)
path = '/Users/dmitry/python_projects/tableau/data/'


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


# for US only
def for_us(source):
    inp_us = source.loc[source['Country/Region'] == 'US']
    inp_us.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
    inp_us.drop(['Country/Region'], axis=1, inplace=True)
    us_agg = inp_us.aggregate(['sum'])
    return us_agg


# for France only
def for_fr(source):
    inp_fr = source.loc[source['Country/Region'] == 'France']
    inp_fr.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
    inp_fr.drop(['Country/Region'], axis=1, inplace=True)
    fr_agg = inp_fr.aggregate(['sum'])
    return fr_agg


def for_world(source):
    inp = source.copy()
    inp.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
    inp.drop(['Country/Region'], axis=1, inplace=True)
    world_agg = inp.aggregate(['sum'])
    return world_agg


def cols_prep_world(sourse):
    data_col = sourse.columns
    data_col = list(data_col)
    return data_col


def val_prep_world(source):
    vals = source.values.tolist()
    vals = vals[0]
    return vals


if __name__ == '__main__':

    print('Do you want to observe ONE country or observe whole WORLD?')
    inp = input()
    inp = inp.lower()

    if inp == 'one':
        print('Enter the name of Country:')
        country = input()
        try:
            country = country.lower().title()

            # USA
            if country == 'Us' or country == 'Usa':
                data = {'Period': cols_prep_world(for_us(conf_all)),
                        'Cases': val_prep_world(for_us(conf_all)),
                        'Deathes': val_prep_world(for_us(d_all))}
                out = pd.DataFrame(data)
                out.to_csv(path + "/covid_USA.csv", index=False)
                print('Your files saved as ' + path + 'covid_USA.csv')
            # FRANCE
            elif country == 'France':
                data = {'Period': cols_prep_world(for_fr(conf_all)),
                        'Cases': val_prep_world(for_fr(conf_all)),
                        'Deathes': val_prep_world(for_fr(d_all))}
                out = pd.DataFrame(data)
                out.to_csv(path + "/covid_France.csv", index=False)
                print('Your files saved as ' + path + 'covid_France.csv')
            else:
                data = {'Period': cols_prep(conf_all),
                        'New_cases': val_prep(conf_all, country),
                        'Deaths': val_prep(d_all, country)}
                out = pd.DataFrame(data)
                out.to_csv(path + "/covid_{0:s}.csv".format(country), index=False)
                print('Your files saved as ' + path + 'covid_{0:s}.csv'.format(country))
        except IndexError:
            print('No such country!')

    elif inp == 'world':
        data = {'Period': cols_prep_world(for_world(conf_all)),
                'Cases': val_prep_world(for_world(conf_all)),
                'Deathes': val_prep_world(for_world(d_all))}
        # 'Recovered': val_prep_world(for_world(r_all))}
        out = pd.DataFrame(data)
        out.to_csv(path + "/covid_WORLD.csv", index=False)
        print('Your files saved as ' + path + 'covid_WORLD.csv')

    # elif inp == "compare" or inp == 'two':
    #     print('Enter first country (but not US):')
    #     country_1 = input()
    #     country_1 = country_1.lower().title()
    #     print('Enter second country (but not US):')
    #     country_2 = input()
    #     country_2 = country_2.lower().title()
    #
    #     try:
    #         data_1 = {'Country': country_1,
    #                   'Period': cols_prep(conf_all),
    #                   'New_cases': val_prep(conf_all, country_1),
    #                   'Deaths': val_prep(d_all, country_1)}
    #                   #'Recovered': val_prep(r_all, country_1)}
    #         data_2 = {'Country': country_2,
    #                   'Period': cols_prep(conf_all),
    #                   'New_cases': val_prep(conf_all, country_2),
    #                   'Deaths': val_prep(d_all, country_2)}
    #                   #'Recovered': val_prep(r_all, country_2)}
    #
    #         out_1 = pd.DataFrame(data_1)
    #         out_2 = pd.DataFrame(data_2)
    #
    #         out_1 = out_1.set_index(['Country', 'Period'])
    #         out_2 = out_2.set_index(['Country', 'Period'])
    #
    #         out_f = out_1.append(out_2)
    #
    #         out_f.to_csv(path + "/covid_{0:s}+{1:s}.csv".format(country_1, country_2))
    #         print('Your files saved as ' + path + 'covid_{0:s}+{1:s}.csv'.format(country_1, country_2))
    #     except IndexError:
    #         print("You've made an error in one of the countries")

    else:
        print('Next time enter only "one", or "world"')
