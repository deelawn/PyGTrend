from GTrend import GTrend

trend1 = GTrend('manchester by the sea')
trend1.set_range('30days')
trend1.retrieve()

print(trend1.raw)
print(trend1.normalized)
print(trend1.time_points)

trend2 = GTrend('moonlight')
trend2.set_range('30days')
trend2.retrieve()

print(trend2.raw)
print(trend2.normalized)
print(trend2.time_points)

corr = trend1.get_corr(trend2)
print(corr)

