MyRiksdag
---------

Some dataanalysis done on open data from the [Swedish Riksdag](https://en.wikipedia.org/wiki/Riksdag).

All the data comes from [data.riksdagen.se](http://data.riksdagen.se/).

![example output plot](https://github.com/ErikBjare/MyRiksdag/raw/master/media/example.png)

## Usage

To use, first run the `get_data.sh` script. When prompted if you want to download & extract the data answer yes.

Then you can run either `python3 main.py` or `python3 agreements.py`.


## Other neat visualizations

 - https://www.svt.se/special/sa-rostade-svenskarna/
 - https://www.svt.se/special/det-politiska-landskapet/


## Crazy idea (MyRiksdag 2.0?)

Sorry for Swedish, sent it to a friend and not keen on translating right now:

> Anta att man hade vetat i förväg hur en viss politiker tänker rösta i en viss fråga, då kan man bygga en app där man kan se/mäta hur bra den politikern passar ens egna preferenser. 
>
> Anta nu att man känner till preferenser av flera politiker, då kan man skriva en app som rekommenderar vilken politiker som minimerar "preferensloss", som man därmed borde rösta på för att maximera att sina preferenser reflekteras i riksdagen. Någon sorts valkompass, fast datan är baserad på hur politiker faktiskt tänker rösta i en votering.

An important problem to consider is that a politician might want to vote like you now, but haven't voted like you wanted in the past.

> Det problemet hade lösts om man räknade med att "straffa" politiker som inte har röstat som du hade velat rösta i en votering. Vi har all data som krävs för att bygga det redan idag, det är att titta framåt och bygga en databas av vad politiker tänker rösta som är klurigt.
