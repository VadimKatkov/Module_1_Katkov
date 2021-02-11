import pandas as pd
import re
import itertools as it
import collections as cl

movies_bd = pd.read_csv(r"D:\SkillFactory\Module1\movie_bd_v5.csv")


# function to process strings like 'cast', 'genres', 'production_companies'
def name_processor(long_string):
    names_list = []
    for row in long_string:
        temp_list = row.split('|')
        for name in temp_list:
            if name in names_list:
                break
            else:
                names_list.append(name)
    return names_list


# Вопрос 1. У какого фильма из списка самый большой бюджет?
print('Вопрос 1. У какого фильма из списка самый большой бюджет?\n',
      movies_bd[['imdb_id', 'original_title', 'budget']][movies_bd.budget == movies_bd.budget.max()])

# Вопрос 2. Какой из фильмов самый длительный (в минутах)?
print('\nВопрос 2. Какой из фильмов самый длительный (в минутах)?\n',
      movies_bd[['imdb_id', 'original_title', 'runtime']][movies_bd.runtime == movies_bd.runtime.max()])

# Вопрос 3. Какой из фильмов самый короткий (в минутах)?
print('\nВопрос 3. Какой из фильмов самый короткий (в минутах)?\n',
      movies_bd[['imdb_id', 'original_title', 'runtime']][movies_bd.runtime == movies_bd.runtime.min()])

# Вопрос 4. Какова средняя длительность фильмов?
print('\nВопрос 4. Какова средняя длительность фильмов?\n',
      round(movies_bd.runtime.mean()), 'мин')

# Вопрос 5. Каково медианное значение длительности фильмов?
print('\nВопрос 5. Каково медианное значение длительности фильмов?\n',
      round(movies_bd.runtime.median()), 'мин')

# Вопрос 6. Какой фильм самый прибыльный?
movies_bd['margin'] = movies_bd.apply(lambda row: row['revenue'] - row['budget'], axis=1)
print('\nВопрос 6. Какой фильм самый прибыльный?\n',
      movies_bd[['imdb_id', 'original_title', 'budget', 'revenue', 'margin']]
      [movies_bd.margin == movies_bd.margin.max()])

# Вопрос 11. Какого жанра фильмов больше всего?
print('\nВопрос 11. Какого жанра фильмов больше всего?')

genres_list = name_processor(movies_bd.genres)
genres_db = pd.DataFrame(genres_list, columns=['genres'])

genres_db['film_count'] = list(map(lambda name:
                                   movies_bd[movies_bd.genres.str.contains(name)]['imdb_id'].count(),
                                   genres_db['genres']))
print(genres_db.sort_values(by='film_count', ascending=False).head(1))

# Вопрос 12. Фильмы какого жанра чаще всего становятся прибыльными?
print('\nВопрос 12. Фильмы какого жанра чаще всего становятся прибыльными?')
genres_db['film_profitable'] = list(map(lambda name: movies_bd[(movies_bd.genres.str.contains(name))
                                                               & (movies_bd.margin > 0)]['imdb_id'].count(),
                                        genres_db['genres']))
print(genres_db.sort_values(by='film_profitable', ascending=False).head(1))

# Вопрос 13. У какого режиссёра самые большие суммарные кассовые сборы?
print('\nВопрос 13. У какого режиссёра самые большие суммарные кассовые сборы?',
      movies_bd.groupby('director').revenue.sum().sort_values(ascending=False).head(1))

# Вопрос 14. Какой режиссер снял больше всего фильмов в стиле Action?
print('\nВопрос 14. Какой режиссер снял больше всего фильмов в стиле Action?\n',
      movies_bd[(movies_bd.genres.str.contains('Action', na=False)) &
                (movies_bd.director.isin(
                    ['Ridley Scott', 'Guy Ritchie', 'Robert Rodriguez', 'Quentin Tarantino', 'Tony Scott']))]
      .director.value_counts().sort_values(ascending=False).head(1))

# Вопрос 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году?
print('\nВопрос 15. Фильмы с каким актером принесли самые высокие кассовые сборы в 2012 году?')

actors_list = name_processor(movies_bd.cast)
actors_db = pd.DataFrame(actors_list, columns=['actor_name'])

actors_db['film_revenue'] = list(map(lambda name: movies_bd[(movies_bd.release_year == 2012)
                                                            & (movies_bd.cast.str.contains(name))].revenue.sum(),
                                     actors_db['actor_name']))

print(actors_db.sort_values(by='film_revenue', ascending=False).head(1))

# Вопрос 16. Какой актер снялся в большем количестве высокобюджетных фильмов?
# Примечание: в фильмах, где бюджет выше среднего по данной выборке.
print('\nВопрос 16. Какой актер снялся в большем количестве высокобюджетных фильмов?')

actors_db['count'] = list(map(lambda name: movies_bd[(movies_bd.budget > movies_bd.budget.mean())
                                                     & (movies_bd.cast.str.contains(name))].imdb_id.count(),
                              actors_db['actor_name']))

print(actors_db.sort_values(by='count', ascending=False).head(5))

# Вопрос 17. В фильмах какого жанра больше всего снимался Nicolas Cage?
# так же можно было сделать через map+lambda  в одну строку, но решил оставить цикл
print('\nВопрос 17. В фильмах какого жанра больше всего снимался Nicolas Cage?')
genres_cage = pd.DataFrame(columns=['genres', 'cage_count'])

for name in genres_list:
    temp = 0
    for row in movies_bd[movies_bd.cast.str.contains('Nicolas Cage', na=False)].genres:
        if row.find(name) != -1:
            temp += 1
    genres_cage.loc[len(genres_cage)] = [name, temp]
print(genres_cage.sort_values(by='cage_count', ascending=False).head(1))

# Вопрос 18. Самый убыточный фильм от Paramount Pictures?
# print(movies_bd.columns)
print('\nВопрос 18. Самый убыточный фильм от Paramount Pictures?')
print(movies_bd[['imdb_id', 'original_title', 'margin']][movies_bd.production_companies.str.contains('Paramount')]
      .sort_values(by='margin', ascending=True).head(1))

# Вопрос 19. Какой год стал самым успешным по суммарным кассовым сборам?
print('\nВопрос 19. Какой год стал самым успешным по суммарным кассовым сборам?')
print(movies_bd.groupby('release_year')['revenue'].sum().sort_values(ascending=False).head(1))

# Вопрос 20. Какой самый прибыльный год для студии Warner Bros?
print('\nВопрос 20. Какой самый прибыльный год для студии Warner Bros?')
print(movies_bd[movies_bd.production_companies.str.contains('Warner Bros')].groupby('release_year')[
          'margin'].sum().sort_values(ascending=False).head(1))
print(type(movies_bd.loc[20, 'release_date']))

# Вопрос 21. В каком месяце за все годы суммарно вышло больше всего фильмов?
print('\nВопрос 21. В каком месяце за все годы суммарно вышло больше всего фильмов?')
# adding column with month number (добавление названия месяца надо было делать через создание дополнительного словаря)
movies_bd['release_month'] = movies_bd.release_date.apply(lambda name: int(re.match(r'\d+/', name)[0].strip('/')))
print(movies_bd.groupby('release_month')['imdb_id'].count().sort_values(ascending=False).head(1))

# Вопрос 22. Сколько суммарно вышло фильмов летом (за июнь, июль, август)?
print('\nВопрос 22. Сколько суммарно вышло фильмов летом (за июнь, июль, август)?')
print(movies_bd[movies_bd.release_month.isin([6, 7, 8])]['imdb_id'].count())

# Вопрос 23. Для какого режиссера зима — самое продуктивное время года?
print('\nВопрос 23. Для какого режиссера зима — самое продуктивное время года?')
print(movies_bd[movies_bd.release_month.isin([12, 1, 2])]
      .groupby('director')['imdb_id'].count().sort_values(ascending=False).head(1))

# Вопрос 24. Какая студия даёт самые длинные названия своим фильмам по количеству символов?
print('\nВопрос 24. Какая студия даёт самые длинные названия своим фильмам по количеству символов?')

movies_bd['name_long'] = movies_bd.original_title.apply(lambda name: len(str(name)))
name_index = movies_bd[movies_bd.name_long == movies_bd.name_long.max()]['production_companies'].index[0]
print('студия: ', movies_bd.loc[name_index, 'production_companies'].split('|'))

# Вопрос 25. Описания фильмов какой студии в среднем самые длинные по количеству слов?
print('\nВопрос 25. Описания фильмов какой студии в среднем самые длинные по количеству слов?')

production_companies_list = name_processor(movies_bd.production_companies)
production_companies_db = pd.DataFrame(columns=['prod_name', 'overview_long'])

for name in production_companies_list:
    temp = 0
    movies_count = 0
    for counter in movies_bd.index:
        if movies_bd.loc[counter, 'production_companies'].find(name) != -1:
            temp += len(movies_bd.loc[counter, 'overview'].split())
            movies_count += 1
    production_companies_db.loc[len(production_companies_db)] = [name, temp / movies_count]

print(production_companies_db[production_companies_db.prod_name.isin
(["Universal Pictures", "Warner Bros", "Midnight Picture Show", "Paramount Pictures", "Total Entertainment"])]
      .sort_values(by='prod_name', ascending=False))

# Вопрос 26. Какие фильмы входят в один процент лучших по рейтингу?
print('\nВопрос 26. Какие фильмы входят в один процент лучших по рейтингу?')

movies_bd['vote_percent'] = movies_bd.vote_average.apply(lambda vote: vote / movies_bd.vote_average.sum())

vote_sum = 0
counter = 0
movies_bd = movies_bd.sort_values(by='vote_percent', ascending=False)

while vote_sum <= 0.01:
    vote_sum += movies_bd.loc[counter]['vote_percent']
    counter += 1
else:
    print(movies_bd[['original_title', 'vote_average', 'vote_percent']].iloc[:counter])

# Вопрос 27. Какие актеры чаще всего снимаются в одном фильме вместе?
# Признаюсь - решение содрал. Но с работой функций разобрался
print('\nВопрос 27. Какие актеры чаще всего снимаются в одном фильме вместе?')
actors_pairs = pd.DataFrame(movies_bd.cast)
actors_pairs['names'] = actors_pairs.cast.apply(lambda names: names.split('|'))
actors_pairs['couples'] = actors_pairs.names.apply(lambda row: list(it.combinations(row, 2)))
actors_pairs = actors_pairs.explode('couples')
print(cl.Counter(actors_pairs.couples).most_common(5))
