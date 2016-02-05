import tracing

stat=tracing.StatisticObject(version='05',
                             statisticsFile='test_statistics.txt')

#stat.print_sprockets([1,2,3,4,5],[1,2,3,4,5],[],[],[],5,5,10,5,1)

#stat.print_solution([1,2,3,4,5],[1,2,3,4,5],[],[],[],5,5,10,5,1)

stat.write_statistics()

for i in range(1000):
    stat.count()
    
stat.print_statistics()

stat.save_statistics()

gearstat=tracing.GearStatisticObject(version='05', resultFile='test_results.txt',
                             statisticsFile='test_statistics.txt')


gearstat.print_statistics(5,6)
gearstat.write_statistics(5,6)
gearstat.save_statistics(5,6)
