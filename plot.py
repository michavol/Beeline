import matplotlib.pyplot as plt
#import seaborn as sns
def main():
    print(5)
    a = [1,2,3,4]
    plt.plot(a,a)
    plt.savefig("h.png")
    plt.show()
    # flights = sns.load_dataset("flights")
    # flights.head()
    # may_flights = flights.query("month == 'May'")
    # sns.lineplot(data=may_flights, x="year", y="passengers")
if __name__ == '__main__':
  main()