var PI = Math.PI;
var TZ = 7;
//var CAN = new Array('Giap','At','Binh','Dinh','Mau','Ky','Canh','Tan','Nham','Quy');
//var CHI = new Array('Ty','Suu','Dan','Mao','Thin','Ty','Ngo','Mui','Than','Dau','Tuat','Hoi');
//var DofW = new Array('Thu hai','Thu ba','Thu bon','Thu nam','Thu sau','Thu bay','Chu nhat');
var CAN = new Array('Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Qúy');
var CHI = new Array('Tý','Sửu','Dần','Mão','Thìn','Tỵ','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi');
var DofW = new Array('Thứ hai','Thứ ba','Thứ bốn','Thứ năm','Thứ sáu','Thứ bảy','Chủ nhật');
//var DofWeng = new Array('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');

function jdFromDate(dd, mm, yy){
    var a, y, m, jd;
    a = INT((14 - mm) / 12);
    y = yy+4800-a;
    m = mm+12*a-3;
    jd = dd + INT((153*m+2)/5) + 365*y + INT(y/4) - INT(y/100) + INT(y/400) - 32045;
    if (jd < 2299161) {
        jd = dd + INT((153*m+2)/5) + 365*y + INT(y/4) - 32083;
    }
    return jd;
}
function jdToDate(jd){
    var a, b, c, d, e, m, day, month, year;
    if (jd > 2299160) { // After 5/10/1582, Gregorian calendar
        a = jd + 32044;
        b = INT((4*a+3)/146097);
        c = a - INT((b*146097)/4);

        b = 0;
        c = jd + 32082;
    }
    d = INT((4*c+3)/1461);
    e = c - INT((1461*d)/4);
    m = INT((5*e+2)/153);
    day = e - INT((153*m+2)/5) + 1;
    month = m + 3 - 12*INT(m/10);
    year = b*100 + d - 4800 + INT(m/10);
    return new Array(day, month, year);
}
function getNewMoonDay(k, timeZone){
    var T, T2, T3, dr, Jd1, M, Mpr, F, C1, deltat, JdNew;
    T = k/1236.85; // Time in Julian centuries from 1900 January 0.5
    T2 = T * T;
    T3 = T2 * T;
    dr = PI/180;
    Jd1 = 2415020.75933 + 29.53058868*k + 0.0001178*T2 - 0.000000155*T3;
    Jd1 = Jd1 + 0.00033*Math.sin((166.56 + 132.87*T - 0.009173*T2)*dr); // Mean new moon
    M = 359.2242 + 29.10535608*k - 0.0000333*T2 - 0.00000347*T3; // Sun's mean anomaly
    Mpr = 306.0253 + 385.81691806*k + 0.0107306*T2 + 0.00001236*T3; // Moon's mean anomaly
    F = 21.2964 + 390.67050646*k - 0.0016528*T2 - 0.00000239*T3; // Moon's argument of latitude
    C1=(0.1734 - 0.000393*T)*Math.sin(M*dr) + 0.0021*Math.sin(2*dr*M);
    C1 = C1 - 0.4068*Math.sin(Mpr*dr) + 0.0161*Math.sin(dr*2*Mpr);
    C1 = C1 - 0.0004*Math.sin(dr*3*Mpr);
    C1 = C1 + 0.0104*Math.sin(dr*2*F) - 0.0051*Math.sin(dr*(M+Mpr));
    C1 = C1 - 0.0074*Math.sin(dr*(M-Mpr)) + 0.0004*Math.sin(dr*(2*F+M));
    C1 = C1 - 0.0004*Math.sin(dr*(2*F-M)) - 0.0006*Math.sin(dr*(2*F+Mpr));
    C1 = C1 + 0.0010*Math.sin(dr*(2*F-Mpr)) + 0.0005*Math.sin(dr*(2*Mpr+M));
    if (T < -11) {
        deltat= 0.001 + 0.000839*T + 0.0002261*T2 - 0.00000845*T3 - 0.000000081*T*T3;
    } else {
        deltat= -0.000278 + 0.000265*T + 0.000262*T2;
    };
    JdNew = Jd1 + C1 - deltat;
    return INT(JdNew + 0.5 + timeZone/24);
}
function getSunLongitude(jdn, timeZone){
    var T, T2, dr, M, L0, DL, L;
    T = (jdn - 2451545.5 - timeZone/24) / 36525; // Time in Julian centuries from 2000-01-01 12:00:00 GMT
    T2 = T*T;
    dr = PI/180; // degree to radian
    M = 357.52910 + 35999.05030*T - 0.0001559*T2 - 0.00000048*T*T2; // mean anomaly, degree
    L0 = 280.46645 + 36000.76983*T + 0.0003032*T2; // mean longitude, degree
    DL = (1.914600 - 0.004817*T - 0.000014*T2)*Math.sin(dr*M);
    DL = DL + (0.019993 - 0.000101*T)*Math.sin(dr*2*M) + 0.000290*Math.sin(dr*3*M);
    L = L0 + DL; // true longitude, degree
    L = L*dr;
    L = L - PI*2*(INT(L/(PI*2))); // Normalize to (0, 2*PI)
    return INT(L / PI * 6);
}
function getLunarMonth11(yy, timeZone){
    var k, off, nm, sunLong;
    off = jdFromDate(31, 12, yy) - 2415021;
    k = INT(off / 29.530588853);
    nm = getNewMoonDay(k, timeZone);
    sunLong = getSunLongitude(nm, timeZone); // sun longitude at local midnight
    if (sunLong >= 9) {
        nm = getNewMoonDay(k-1, timeZone);
    }
    return nm;
}
function getLeapMonthOffset(a11, timeZone){
    var k, last, arc, i;
    k = INT((a11 - 2415021.076998695) / 29.530588853 + 0.5);
    last = 0;
    i = 1; // We start with the month following lunar month 11
    arc = getSunLongitude(getNewMoonDay(k+i, timeZone), timeZone);
    do {
        last = arc;
        i++;
        arc = getSunLongitude(getNewMoonDay(k+i, timeZone), timeZone);
    } while (arc != last && i < 14);
    return i-1;
}
function convertSolar2Lunar(dd, mm, yy, timeZone){
    var k, dayNumber, monthStart, a11, b11, lunarDay, lunarMonth, lunarYear, lunarLeap;
    dayNumber = jdFromDate(dd, mm, yy);
    k = INT((dayNumber - 2415021.076998695) / 29.530588853);
    monthStart = getNewMoonDay(k+1, timeZone);
    if (monthStart > dayNumber) {
        monthStart = getNewMoonDay(k, timeZone);
    }
    a11 = getLunarMonth11(yy, timeZone);
    b11 = a11;
    if (a11 >= monthStart) {
        lunarYear = yy;
        a11 = getLunarMonth11(yy-1, timeZone);
    } else {
        lunarYear = yy+1;
        b11 = getLunarMonth11(yy+1, timeZone);
    }
    lunarDay = dayNumber-monthStart+1;
    diff = INT((monthStart - a11)/29);
    lunarLeap = 0;
    lunarMonth = diff+11;
    if (b11 - a11 > 365) {
        leapMonthDiff = getLeapMonthOffset(a11, timeZone);
        if (diff >= leapMonthDiff) {
            lunarMonth = diff + 10;
            if (diff == leapMonthDiff) {
                lunarLeap = 1;
            }
        }
    }
    if (lunarMonth > 12) {
        lunarMonth = lunarMonth - 12;
    }
    if (lunarMonth >= 11 && diff < 4) {
        lunarYear -= 1;
    }
    return new Array(lunarDay, lunarMonth, lunarYear, lunarLeap);
}
function convertLunar2Solar(lunarDay, lunarMonth, lunarYear, lunarLeap, timeZone){
    var k, a11, b11, off, leapOff, leapMonth, monthStart;
    if (lunarMonth < 11) {
        a11 = getLunarMonth11(lunarYear-1, timeZone);
        b11 = getLunarMonth11(lunarYear, timeZone);
    } else {
        a11 = getLunarMonth11(lunarYear, timeZone);
        b11 = getLunarMonth11(lunarYear+1, timeZone);
    }
    off = lunarMonth - 11;
    if (off < 0) {
        off += 12;
    }
    if (b11 - a11 > 365) {
        leapOff = getLeapMonthOffset(a11, timeZone);
        leapMonth = leapOff - 2;
        if (leapMonth < 0) {
            leapMonth += 12;
        }
        if (lunarLeap != 0 && lunarMonth != leapMonth) {
            return new Array(0, 0, 0);
        } else if (lunarLeap != 0 || off >= leapOff) {
            off += 1;
        }
    }
    k = INT(0.5 + (a11 - 2415021.076998695) / 29.530588853);
    monthStart = getNewMoonDay(k+off, timeZone);
    return jdToDate(monthStart+lunarDay-1);
}
function INT(d){
    return Math.floor(d);
}
function testData(form,d,str,label) {
    if (!isFinite(d)){
        form.text.value = label;
        alert(str);
        return true;
    }
    if( d == ""){
        form.text.value = label;
        alert(str);
        return true;
    }
}
function testDayOfMonth(form,d,m,y,str,label){
    if(d<=0 || m <= 0 || m>12){alert(str);form.text.value = label;return true;}
    if(m == 2 && (y%4)==0 && d>29){alert(str);form.text.value = label;return true;}
    if(m == 2 && (y%4)!=0 && d>28){alert(str);form.text.value = label;return true;}
    array31 = new Array(1,3,5,7,8,10,12);
    array30 = new Array(4,6,9,11);
    for(i=0;i<array31.length;i++){
        if(m == array31[i] && d > 31){alert(str);form.text.value = label;return true;}
    }
    for(i=0;i<array30.length;i++){
        if(m == array30[i] && d > 30){alert(str);form.text.value = label;return true;}
    }

}
function testDouble(form,d,str,label){
    if( Math.floor(d) != d){alert(str);form.text.value = label;return true;}
}
function printAm(form){
    var str = "Nhập vào ngày dương lịch không chính xác";
    var label_result = "Kết quả tìm ngày âm lịch";
    d = (form.day.value);
    m = (form.month.value);
    y = (form.year.value);
    if(testData(form,d,str,label_result)) return;if(testData(form,m,str,label_result)) return;
    if(testData(form,y,str,label_result)) return;

    d = eval(d); m = eval(m); y = eval(y);

    if(testDayOfMonth(form,d,m,y,str,label_result)) return;
    if(testDouble(form,d,str,label_result)) return;if(testDouble(form,m,str,label_result)) return;
    if(testDouble(form,y,str,label_result)) return;
    if(y<1000 || y > 2999){alert("Chỉ xem tối đa từ năm 1000 đến năm 2999");return;}
    AL = convertSolar2Lunar(d,m,y,TZ);
    str = "Ngày âm lịch cần tìm:" + "\n";
    str += dayOfWeek(d,m,y) + "\n";
    str += "Ngày: " +  AL[0] + " - ";
    str += canDay(d,m,y) + " " + chiDay(d,m,y) + '\n';
    str += "Tháng: " + AL[1] +'(' + testMoon(d,m,y,AL[0],AL[3]) + ") - " + canMonth(AL[1],AL[2]) + " " + chiMonth(AL[1]);
    str += '\nNăm: ' + AL[2] + " - " + canYear(AL[2]) + " " + chiYear(AL[2]);
    form.text.value = str;
}

////////// them///////////////
function testNamNhuan(yyyy){
    var jd1 = getLunarMonth11(yyyy-1,TZ);
    var jd2 = getLunarMonth11(yyyy,TZ);
    if( (jd2 - jd1) > 365 ) return getLeapMonthOffset(jd1,TZ) -2;
    else return -10;
}
function testMoon(dd,mm,yy,dL,nhuan){
    var jd = jdFromDate(dd,mm,yy);
    var dau1 = dauThangAm(jd);
    var dau2 = dau1+45;
    dau2 = dauThangAm(dau2);
    var hieu = dau2-dau1;
    str = "";
    if(nhuan == 1)
        str = "nhuận - ";
    if(hieu == 29)
        str += "thiếu";
    else if(hieu == 30)
        str += "đủ";
    else str += "false";
    return str;
}
function canYear(yL){
    return CAN[(yL + 6) % 10];
}
function chiYear(yL){
    return CHI[(yL + 8) % 12];
}
function canMonth(mL,yL){
    return CAN[(12 * yL + 3 + mL) % 10];
}
function chiMonth(mL){
    return CHI[(mL + 1) % 12]
}
function canDay(dd,mm,yy){
    return CAN[(jdFromDate(dd,mm,yy) + 9) %10];
}
function chiDay(dd,mm,yy){
    return CHI[(jdFromDate(dd,mm,yy) + 1) % 12];
}
function dayOfWeek(dd,mm,yy){
    return DofW[jdFromDate(dd,mm,yy) % 7];
}
function dauThangAm(jd){
    var k = INT((jd - 2415021)/29.530588853);
    return getNewMoonDay(k,TZ);
}