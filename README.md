# gpc2csv	

Převodník výpisů bankovních transakcí (výpisů z účtu) ze standardizovaného bankovního formátu ABO do formátu CSV (textový formát s čárkou oddělenými hodnotami). CSV formát může být následně otevřen tabulkovým procesorem (Microsoft Excel, LibreOffice Calc, ...) k dalším úpravám a analýze.

## Co je ABO formát

ABO formát (ABO = automatické bankovní operace) byl vytvořen Českou národní bankou pro standardizovanou výměnu informací o bankovních operacích. Formát popisuje jak aktivní operace (zadávání příkazů k úhradě), tak opearace pasivní (výpisy pohybů na účtu). 

Výpis operací provedených na bankovním účtu ve formátu ABO (obvyklá přípona souboru je .gpc) lze exportovat z většiny internetových bankovnictví českých bank a importovat do mnoha účetních programů. Jde o čistě textový formát s pevnou šířkou polí kde jeden řádek představuje jeden záznam. Každý ze záznamů se dělí na pole, které mají pevnou délku. Formát byl původně určen pouze pro tuzemský mezibankovní styk, ale obsahuje rozšíření i pro mezinárodní SEPA platby.

## Převod ABO formátu do CSV formátu

Přestože lze bankovní výpisy v ABO formátu načíst mnohými účetními programy, nelze v nich většinou provádět podrobnější analýzy, filtrovat záznamy apod. K těmto účelům se výborně hodí tabulkové procesory typu Excel, které ovšem zase neumí načíst ABO soubory. Pomocí tohoto převodního programu lze transakční údaje z ABO souboru převést do formátu [CSV](https://cs.wikipedia.org/wiki/CSV), který lze otevřít v libovolném tabulkovém procesoru, kde lze s daty dále pracovat.

Skript z ABO souboru vybere pouze řádky s kódem 075, tedy věty obsahující údaje o provedených transakcích. 

Ve sloupci označeném jako "kód účtování" je uvedeno, o jaký typ operace se jedná: 1=debetní (odchozí) položka, 2=kreditní (příchozí) položka, 4=storno debetní položky, 5=storno kreditní položky. Částky debetních položek (kódy 1 a 4) jsou v CSV formátu uvedeny jako záporná čísla (s mínusem).

Sloupec "pořadové číslo" udává identifikátor transakce banky a může mít skrytý význam, tj. nemusí se nutně jednat o vzrůstající číselnou řadu. U některých bank toto pole obsahuje kromě pořadí transakce i informaci, zda šlo o jednorázový, trvalý nebo inkasní příkaz, apod.

## Použití
Skript je napsán v jazyce [Python3](https://python.org). Jako parametr je nutné uvést jméno ABO souboru obsahující transakční výpisy. Druhý parametr je volitelný a udává jméno souboru, do kterého je uložen CSV výstup. Není-li druhý parametr uveden, výstup je zobrazen na konzoli.
    
    # načtení ABO souboru a vypsání výstupu na obrazovku
    python3 gpc2csv vstup.gpc
    
    # načtení ABO souboru a vypsání výstupu do souboru
    python3 gpc2csv vstup.gpc vystup.csv

U vstupního souboru se předpokládá kódování Windows1250; pokud je jiné, je třeba upravit skript - viz konstanta INPUT_ENCODING v záhlaví skriptu a [seznam kodeků Pythonu](https://docs.python.org/3/library/codecs.html#standard-encodings). Výstup je v kódování UTF-8. Pozn.: kódování se týká pouze jedné položky - názvu účtu prostistrany.

## Další odkazy

* [Popis ABO formátu výpisů - ČSOB](https://www.csob.cz/portal/documents/10710/1927786/format-gpc.pdf)
* [PHP skript pro načítání ABO výpisů Fio banky](https://wiki.zdechov.net/GPC_export_z_Fio_banky)
* [Převod TXT výpisu ČSOB do ABO formátu](https://github.com/jvimr/csob-txt2gpc)

