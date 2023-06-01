/*
 * This is the code for the SSP project exam by groupe 261. June 2023
 * 
 * This code is used in a prototype for our propoced product for the exam. The proposed product 
 * is a clothes folding machine, but the prototype controlled with this code is simply designed 
 * to present the idea behind the clothes folding machine.
 * 
 * 
 * The code is also build with the idea of further implementation, and contains classes which 
 * could translate well into an expansion of the idea.
 * 
 * 
 * The following naming system has been used for this code.
 * Variables: snake_Case
 * Functions: Pascal_Snake_Case
 * Classes: PascalCase
 * Objects: PascalCase
 * 
 * 
 */





//This is the first class. The first to variables in this class are private, and this is because they
//are used in a function in the class, and only needs to be accessed by the motor itself.
//The remaining variables are public, and will be determined outside of the class.
class Motors {
    int tid_Start;
    int tid_Nu;
  public:
    String navn;              //navn på motoren
    int rotation_Naaet;       //Tidsvariabel for hvor længe en motor skal være tændt før rotationen er nået.
    int input_Pin;            //Den pin vi styrer motoren på

//Here we see the object instansiator, This "function"  is called while instansiating the object, and sets values for the variables inside the class.
//Without these, the object would self instasiate the objects with empty strings or "0" values and the sorts.
    Motors (String N, int R, int I) {
      navn = N;
      rotation_Naaet = R;
      input_Pin = I;
    }


//funktionen der tænder for motoren Her ses det at den har rotation_Naaet og input_Pin som input, og den bruger disse til at udskrive et 5v DC signal 
//til den "motor" som functionen er kaldt igennem.
    void Motor_On_Off(int rotation_Naaet, int input_Pin) {
      tid_Start = millis();
      tid_Nu = tid_Start;

      while ((tid_Nu - tid_Start) < rotation_Naaet) {
        pinMode(input_Pin, HIGH);
        digitalWrite(input_Pin, HIGH);
        tid_Nu = millis();

      }
      Serial.print("input_Pin = ");
      Serial.println(input_Pin);
      digitalWrite(input_Pin, LOW);
      return;
    }
};

//Denne classe er et barn af classen motors, og indeholder derfor alle de samme variabler og functioner som denne. Derfor ser vi også ": Motors("", 0, 0)" 
//der initialiser de variabler fra motors, men blot som ingenting. dette gøres blot for at have styr på at de er defineret som nul da de ikke bruges i koden.
//Det eneste som folder faktisk bruger fra motors er dens Motor_On_Off() funktion. her ser vi at den bruger den egne variabler som input i funktionen.
//Det er Fold() funktionen der sammen med raekke arrayet bestemmer hvilken moter der skal tændes
class Folder: public Motors {
  public:
    int raekke[5]; //array der kan holde en rækkefølge motorene skal tændes i
    int raat[5];  //array der holder værdier for vinklen motorene skal dreje med
    int pins[5]; //array der holder de pins der skal skrives til for at styre motorene
    Folder(int R[5], int RA[5], int P[5])
      : Motors("", 0, 0)
    {
      raekke[0] = R[0];
      raekke[1] = R[1];
      raekke[2] = R[2];
      raekke[3] = R[3];
      raekke[4] = R[4];

      raat[0] = RA[0];
      raat[1] = RA[1];
      raat[2] = RA[2];
      raat[3] = RA[3];
      raat[4] = RA[4];

      pins[0] = P[0];
      pins[1] = P[1];
      pins[2] = P[2];
      pins[3] = P[3];
      pins[4] = P[4];
    }
    void Fold(int Raekke[5], int Raat[5], int Pins[5]) {
      for (int i = 0; i <= 4; i++) {
        if (Raekke[i] >= 0) {
          Motor_On_Off(Raat[Raekke[i]], Pins[Raekke[i]]);
        }
      }
    }
};









//Clothes classen er taget med for at udvide antal af klasse, og kunne evt. bruges til at beskrive nærmest alle tøjformer
//alle den variabler er noget der oversætter til alle slags tøj, og kan derfor bruges som overklasse til Foldable_Clothes som kommer lige under.
class Clothes {
  public:
    String brand;
    String material;
    String type;
    bool foldable;


};


//Foldeable_Clothes er klassen med kun de tøjformer som vores produkt skal kunne folde. I instansiatoren ser vi at den giver alle tøjstykkerne en defination
//men også at den tilføjer et arreay som kun de foldelige tøjstykker har, nemlig rækkefølgen de skal foldes i.
class Foldable_Clothes: public Clothes {
  public:
    int raekkefoelge_For_Fold[5];
    Foldable_Clothes (String B, String M, String T, bool F, int RFF[5]) {
      brand = B;
      material = M;
      type = T;
      foldable = F;
      brand = B;
      raekkefoelge_For_Fold[0] = RFF[0];
      raekkefoelge_For_Fold[1] = RFF[1];
      raekkefoelge_For_Fold[2] = RFF[2];
      raekkefoelge_For_Fold[3] = RFF[3];
      raekkefoelge_For_Fold[4] = RFF[4];
    }



};



//Vores identifier modul er også blevet smidt i en klasse, her kunne man nemlig forstille sig at et lignende modul kunne udvikles, som evt. kunne bruges denne klasses
//funktioner og variabler til at vidderebygge produktet.
class Identifier {
    int toej_Vaerdi; //Denne værdi bliver bestemt ud fra hvilken tøjtype der bliver identificeret. kan udskiftes med clothing_Type[] hvis switch casen i loopet bliver lavet om
    int pin_Aflaesning[6];
  public:
    int state;                // 1 hvis fold er i gang 0 hvis den venter på input
    int antal;                //stk. tøj den har foldet
    byte output_Pin_LDR_Sensor[6];
    String clothing_Type[7];
    int light_Value;

    Identifier (int S, int A, byte P[6], String C[7], int l_V) {
      state = S;
      antal = A;
      output_Pin_LDR_Sensor[0] = P[0];
      output_Pin_LDR_Sensor[1] = P[1];
      output_Pin_LDR_Sensor[2] = P[2];
      output_Pin_LDR_Sensor[3] = P[3];
      output_Pin_LDR_Sensor[4] = P[4];
      output_Pin_LDR_Sensor[5] = P[5];
      clothing_Type[0] = C[0];
      clothing_Type[1] = C[1];
      clothing_Type[2] = C[2];
      clothing_Type[3] = C[3];
      clothing_Type[4] = C[4];
      clothing_Type[5] = C[5];
      clothing_Type[6] = C[6];
      light_Value = l_V;
    }


// Denne funktion opdatere de læste værdier. der er smidt to ekstra tal ind 100 og 500 fordi sensorværdierne ændrede sig efter smalingen af kassen
// Hvis der er problemer med systemet, kan serial.println i funktionen slåes til og sensorenes data kan da manipuleres så de passer med light_Value
    void UpdateValues() {
      pin_Aflaesning[0] = analogRead(output_Pin_LDR_Sensor[0]);
      pin_Aflaesning[1] = analogRead(output_Pin_LDR_Sensor[1]) + 100;
      pin_Aflaesning[2] = analogRead(output_Pin_LDR_Sensor[2]);
      pin_Aflaesning[3] = analogRead(output_Pin_LDR_Sensor[3]);
      pin_Aflaesning[4] = analogRead(output_Pin_LDR_Sensor[4]) + 550;
      pin_Aflaesning[5] = analogRead(output_Pin_LDR_Sensor[5]);
      Serial.println(String(pin_Aflaesning[0]) + " " + String(pin_Aflaesning[1]) + " " + String(pin_Aflaesning[2]) + " " + String(pin_Aflaesning[3]) + " " + String(pin_Aflaesning[4]) + " " + String(pin_Aflaesning[5]));
    }

//I denne function kigger vi efter om en af sensorene bliver højere end den valgt light_Value hvilket betyder at et "stykke tøj" dækker sensoren
//Herefter aflæser den hvilken pin dette sker på for at differentiere de forskellige tøjtyper, og returnere derefter en værdi tilsvarende til dette.
//I tilfælde at at ingen af værdierne er højere returneres nul og der skrives klar på seriel monitoren
    int Identify_Clothes() {
      if ( light_Value < pin_Aflaesning[0] || light_Value < pin_Aflaesning[1] || light_Value < pin_Aflaesning[2] || light_Value < pin_Aflaesning[3] || light_Value < pin_Aflaesning[4] || light_Value < pin_Aflaesning[5]) {
        state = 1;
        for (int i = 0; i <= 5; i++) {
          if (light_Value < pin_Aflaesning[i]) {
            switch (i) {
              case 0:
                Serial.println(clothing_Type[1]);
                toej_Vaerdi = 1;
                break;
              case 1:
                Serial.println(clothing_Type[2]);
                toej_Vaerdi = 2;
                break;
              case 2:
                Serial.println(clothing_Type[3]);
                toej_Vaerdi = 3;
                break;
              case 3:
                Serial.println(clothing_Type[4]);
                toej_Vaerdi = 4;
                break;
              case 4:
                Serial.println(clothing_Type[5]);
                toej_Vaerdi = 5;
                break;
              case 5:
                Serial.println(clothing_Type[6]);
                toej_Vaerdi = 6;
                break;
            }
            antal += 1;
            state = 0;
            Serial.println("antal = " + String(antal));
            return toej_Vaerdi;
          }
        }
      }
      else {
        Serial.println(clothing_Type[0]);
        toej_Vaerdi = 0;
        return toej_Vaerdi;
      }
    }
};


// Tøjtypernes folderækkefølge
int foldable_Clothes_Array_Bukser[5]         = {0, 1, 2, 3, 4};
int foldable_Clothes_Array_Tshirt[5]         = {1, 2, 3, 4, 0};
int foldable_Clothes_Array_Viskestykke[5]    = {2, 3, 4, 0, 1};
int foldable_Clothes_Array_Undertoej[5]      = {3, 4, 0, 1, 2};
int foldable_Clothes_Array_Haettetroeje[5]   = {4, 0, 1, 2, 3};
int foldable_Clothes_Array_Shorts[5]         = {4, 3, 2, 1, 0};

//Pins sensorene læses på
byte identifier_Byte_Array[6]                = {A0, A1, A2, A3, A4, A5};
//Tøjtyperne vi kan folde
String identifier_String_Array[7]            = {"klar", "Bukser", "T-shirt", "Viskestykke", "Undertøj", "Hættetrøje", "Shorts"};


//Dette array bruges kun til at initialisere objektet folder1
int folder_Array1[5]                         = {0, 0, 0, 0, 0};

//folder1 objekted instansieres med rent nul værdier
Folder folder1(folder_Array1, folder_Array1, folder_Array1);

//motorene instansieres med navn, værdi for rotation_naaet, og en inputpin
Motors motor1("Foerste Motor", 250, 2);
Motors motor2("Anden Motor", 250, 3);
Motors motor3("Tredje Motor", 250, 4);
Motors motor4("Fjerde Motor", 250, 5);
Motors motor5("Femte Motor", 250, 6);

//Tøj instansieres med brand, materiale, type, foldabillity, og en rækkefølge der kan folde tøjet.
Foldable_Clothes Bukser1("Levi's", "Denim", "Bukser", true, foldable_Clothes_Array_Bukser);
Foldable_Clothes Tshirt1("Polo", "Bomuld", "Tshirt", true, foldable_Clothes_Array_Tshirt);
Foldable_Clothes Viskestykke1("Jysk", "bomuld", "Viskestykke", true, foldable_Clothes_Array_Viskestykke);
Foldable_Clothes Undertoej1("Victoria's secret", "Silke", "Undertoej", true, foldable_Clothes_Array_Undertoej);
Foldable_Clothes Haettetroeje1("Superdry", "Bomuld", "Haettetroeje", true, foldable_Clothes_Array_Haettetroeje);
Foldable_Clothes Shorts1("Levi's", "Denim", "Shorts", true, foldable_Clothes_Array_Shorts);

//identifieren instansieres med state 0 og antal 0, de pins sensorene måles på, de tøjtyper der kan foldes, og en Light_value for den givne belysning omkring kassen.
Identifier Identifier1(0, 0, identifier_Byte_Array, identifier_String_Array, 850);

//arrays der indeholder alle motorenes Pins, bruges til når de skal implementeres i funktionen Fold() fra Folder folder1.Fold()
int motor_Pin_Array[5] = {motor1.input_Pin, motor2.input_Pin, motor3.input_Pin, motor4.input_Pin, motor5.input_Pin};
int motor_Raat_Array[5] = {motor1.rotation_Naaet, motor2.rotation_Naaet, motor3.rotation_Naaet, motor4.rotation_Naaet, motor5.rotation_Naaet};



/*
void folder(int Raekke[5], int raat[5], int Pins[5]) {
  for (int i = 0; i <= 4; i++) {
    if (Raekke[i] > 0) {
      motor1.Motor_On_Off(raat[Raekke[i]], Pins[Raekke[i]]);
    }
  }
}
*/




void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  millis();
}





void loop() {
  delay(2000);
  Identifier1.UpdateValues();

  int A = Identifier1.Identify_Clothes();
  switch (A) {
    case 0:
      Serial.println("0");
      break;
    case 1:
      Serial.println("1");
      folder1.Fold(Bukser1.raekkefoelge_For_Fold, motor_Raat_Array, motor_Pin_Array);
      break;
    case 2:
      Serial.println("2");
      folder1.Fold(Tshirt1.raekkefoelge_For_Fold, motor_Raat_Array, motor_Pin_Array);
      break;
    case 3:
      Serial.println("3");
      folder1.Fold(Viskestykke1.raekkefoelge_For_Fold, motor_Raat_Array, motor_Pin_Array);
      break;
    case 4:
      Serial.println("4");
      folder1.Fold(Undertoej1.raekkefoelge_For_Fold, motor_Raat_Array, motor_Pin_Array);
      break;
    case 5:
      Serial.println("5");
      folder1.Fold(Haettetroeje1.raekkefoelge_For_Fold, motor_Raat_Array, motor_Pin_Array);
      break;
    case 6:
      Serial.println("5");
      folder1.Fold(Shorts1.raekkefoelge_For_Fold, motor_Raat_Array, motor_Pin_Array);
      break;
  }


  delay(200);

}
