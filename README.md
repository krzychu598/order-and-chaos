# Porządek i Chaos
## Krzysztof Wnorowski 04300602117

## Opis projektu
Projekt to prosta gra porządek i chaos stworzona w bibliotece pygame

Gra polega w przypadku grania porządkiem na ustawieniu 5 tych samych znaków w jednej linii, natomiast grając chaosem na niedopuszczenie do takiego ustawienia. Można dowolnie wybierać między znakami. Pole ma wymiary 6x6.

Dostępne są trzy tryby. Gra przeciwko innemu ludzkiemu graczowi, gra przeciwko komputerowi robiącemu losowe ruchy i gra przeciwko komputerowi z prostym algorytmem 

## Działanie kodu
Projekt podzielony jest na 5 modułów
moduł constants ustala niektóre stałe i ładuje pliki graficzne
moduł game to główny plik, który inicjalizuje pygame, wyświetla ekran gry, konwertuje pliki graficzne i włącza dźwięki (każdy użyty dźwięk jest w wolnym dostępie)
W module functions znajduje się logika całego projektu. Klasa StateOfTheGame monitoruje zmiany w stanie gry, wiele mniejszych funkcji usprawnia komunikację między modułami. Znajdziemy też tu funkcje ułatwiające renderowanie napisów i prostokątów interaktywnych. Ostatecznie znaleźć można też funkcje sprawdzające czy ktoś wygrał rozgrywkę oraz decydujące o kolejnych ruchach komputera.
Moduł scenes zawiera klasy reprezentujące kolejne części rozgrywki. Każda z nich jest podklasą nadklasy Scene. W Menu wybieramy ccy chcemy grać porządkiem czy chaosem. Natępnie w ChooseMode wybieramy przeciwko komu chcemy grać, a w klasie game odbywa się rozgrywka. Renderowana jest plansza do gry. Respektowany input to klikanie na kwadraty gdzie chcemy ustawić symbol i naciśnięcie spacji która zmienia bieżący symbol. W końu w klasie GameOver możemy zdecydować czy kontynuujemy czy kończymy rozgrywkę.
Moduł Square zawiera klasę Square. Jest to podklasa Sprite z biblioteki pygame i każda instancja jest modyfikowalna. Po naciśnięciu przez gracza lub wybraniu przez ai zmienia wyświetlany obraz na ten przedstawiający symbol-- kółko lub krzyżyk

## Instrukcja
projekt powinien być uruchomiony z modułu game.py. W przypadku uruchomienia w środowisku innym niż Windows dźwięki mogą nie działać, jednak gra pozostanie funkcjonalna. Wyświetlony ekran jest interaktywny. Wszelkie pola należy wybrać lewym kliknięciem myszy. Naciśnięcie spacji powoduje zmianę wybranego symbolu.

## Przebieg tworzenia projektu
Na wstępie zamierzałem zrobić projekt przy pomocy biblioteki tkinter. Ostatecznie jednak wybrałem pygame, ponieważ nie byłem wcześniej z tą biblioteką zaznajomiony i chciałem spróbować czegoś nowego. Trudno było odpowiednio porozdzielać projekt na moduły. Biblioteka pygame niestety nie ułatwia komunikacji między nimi. Z tej samej racji nie byłem wstanie napisać wiele testów. Funkcje często musiały odwoływać do zmiennych z innych klas. Udało mi się jednak zrobić mechanizmy działające na tyle ogólnych zasadach, że są one aplikowalne do różnych rozmiarów planszy. Polecam poeksperymentować zmieniając stałe SIZE i TO_WIN w module constants.py. Algorytm decydujący o najlepszym ruchu sprawuje się nawet przy planszach małych (np. SIZE = 4, TO_WIN = 4) czy bardzo dużych (np. SIZE = 10, TO_WIN = 8). Sporym problemem miała okazać się implementacja dźwięków. Z niezrozumiałego mi powodu nie działają one w środowisku Linux, ale działają bezproblemowo na Windows. Musi być to jakiś problem pygame.mixer.
