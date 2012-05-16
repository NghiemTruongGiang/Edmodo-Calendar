function userEvent(value){
    if(value == 'logout'){
        parent.location='/logout/';
    }
    if(value == 'setting'){
        window.open('/settings');
    }
    if(value == 'username'){
        parent.location='/';
    }
}
function changeYear(value){
    parent.location='/'+ value+ '/';
}
function changeMonth(form){
    m = form.month.value;
    y = form.year.value;
    parent.location='/month/'+ y + '/' + m;
}
function changeMonthGroup(form){
    m = form.month.value;
    y = form.year.value;
    group = form.group_name.value
    parent.location='/'+ group + '/month/'+ y + '/' + m;
}
function notMonth(){
    alert("Mời bạn kick vào ô khác");
}
function changeMonthGroup(form){
    m = form.month.value;
    y = form.year.value;
    name = form.group_name.value;
    parent.location = '/' + name + '/month/' + y + '/' + m;
}

//////// Lich Viet Nam
//var CAN = new Array('Giap','At','Binh','Dinh','Mau','Ky','Canh','Tan','Nham','Quy');
//var CHI = new Array('Ty','Suu','Dan','Mao','Thin','Ty','Ngo','Mui','Than','Dau','Tuat','Hoi');
//var DofW = new Array('Thu hai','Thu ba','Thu bon','Thu nam','Thu sau','Thu bay','Chu nhat');
//var DofWeng = new Array('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday');
var CAN = new Array('Giáp','Ất','Bính','Đinh','Mậu','Kỷ','Canh','Tân','Nhâm','Qúy');
var CHI = new Array('Tý','Sửu','Dần','Mão','Thìn','Tỵ','Ngọ','Mùi','Thân','Dậu','Tuất','Hợi');
var DofW = new Array('Thứ hai','Thứ ba','Thứ bốn','Thứ năm','Thứ sáu','Thứ bảy','Chủ nhật');
function ad(form){
    form.result.value = "Kết quả tìm ngày dương lịch";
}
function da(form){
    form.result.value = "Kết quả tìm ngày âm lịch";
}
function testData(form,d,str,label) {
    if (!isFinite(d)){
        form.result.value = label;
        alert(str);
        return true;
    }
    if( d == ""){
        form.result.value = label;
        alert(str);
        return true;
    }
}
function testDayOfMonth(form,d,m,y,str,label){
    if(d<=0 || m <= 0 || m>12){alert(str);form.result.value = label;return true;}
    if(m == 2 && (y%4)==0 && d>29){alert(str);form.result.value = label;return true;}
    if(m == 2 && (y%4)!=0 && d>28){alert(str);form.result.value = label;return true;}
    array31 = new Array(1,3,5,7,8,10,12);
    array30 = new Array(4,6,9,11);
    for(i=0;i<array31.length;i++){
        if(m == array31[i] && d > 31){alert(str);form.result.value = label;return true;}
    }
    for(i=0;i<array30.length;i++){
        if(m == array30[i] && d > 30){alert(str);form.result.value = label;return true;}
    }

}
function testDouble(form,d,str,label){
    if( Math.floor(d) != d){alert(str);form.result.value = label;return true;}
}
function vietNamCalendar(form){
    if(document.VietnamCalendar.typeConvert[0].checked == true){
        form.result.value = "Kết quả tìm ngày âm lịch";
        duongAm123(form);
    }
    else{
        form.result.value = "Kết quả tìm ngày dương lịch";
        amDuong123(form);
    }
}
function duongAm123(form){
    var label_result = "Kết quả tìm ngày âm lịch";
    var str = "Nhập vào ngày dương lịch không chính xác";
    var d,m,y;
    d = (form.day.value);
    m = (form.month.value);
    y = (form.year.value);
    if(testData(form,d,str,label_result)) return;
    if(testData(form,m,str,label_result)) return;
    if(testData(form,y,str,label_result)) return;

    d = eval(d); m = eval(m); y = eval(y);
    if(testDayOfMonth(form,d,m,y,str,label_result)) return;
    if(testDouble(form,d,str,label_result)) return;
    if(testDouble(form,m,str,label_result)) return;
    if(testDouble(form,y,str,label_result)) return;

    if(y<1000 || y > 2999){alert("Chỉ xem tối đa từ năm 1000 đến năm 2999");return;}

    AL = convertSolar2Lunar(d,m,y,TZ);
    canChi = canChiAm(d,m,y,AL[0],AL[1],AL[2],AL[3]);
    str = "Ngày âm lịch cần tìm:" + "\n";
    str += dayOfWeek(d,m,y) + "\n";
    str += "Ngày: "+ + AL[0] + " - " + canChi[0] + "\n";
    str += "Tháng: " + AL[1] + " - " +canChi[1] + "\n";
    str += "Năm: " + AL[2] + " - " + canChi[2];
    form.result.value = str;
}
function amDuong123(form){
    var label_result = "Kết quả tìm ngày dương lịch";
    var str = "Nhập vào ngày âm lịch không chính xác";
    var d,m,y;
    d = (form.day.value);
    m = (form.month.value);
    y = (form.year.value);
    if(testData(form,d,str,label_result)) return;
    if(testData(form,m,str,label_result)) return;
    if(testData(form,y,str,label_result)) return;

    d = eval(d); m = eval(m); y = eval(y);
    if( d < 0 || m < 0 ){
        alert(str);
        form.result.value = label_result;
        return;
    }
    if(testDouble(form,d,str,label_result)) return;
    if(testDouble(form,m,str,label_result)) return;
    if(testDouble(form,y,str,label_result)) return;
    if(y<1000 || y > 2999){alert("Chỉ xem tối đa từ năm 1000 đến năm 2999");return;}

    var jdSolar = convertLunar2Solar(d,m,y,0,TZ);
    var dateSolar = jdToDate(jdSolar);
    var nhuan = testNamNhuan(dateSolar[2]);
    if(nhuan != 10){
        if(m == nhuan){
            var temp = "Tháng " + m + "(âm) của năm " + y + " là tháng nhuận";
            temp += "\nBạn muốn chuyển đổi ngày của tháng nhuận";
            if(confirm(temp)){
                jdSolar = convertLunar2Solar(d,m,y,1,TZ);
                dateSolar = jdToDate(jdSolar);
            }
        }
    }
    var checkMonth = testM_full(dateSolar[0],dateSolar[1],dateSolar[2]);
    if(checkMonth == false){
        if(d>29){
            alert(str);
            form.result.value = label_result;
            return;
        }
    }
    else{
        if(d>30){
            alert(str);
            form.result.value = label_result;
            return;
        }
    }
    str = "Ngày dương lịch cần tìm:\n";
    str += dayOfWeek(dateSolar[0],dateSolar[1],dateSolar[2]) + "\n";
    str += "Ngày " + dateSolar[0] + "/" + dateSolar[1] + "/" + dateSolar[2];
    form.result.value = str;
}

function canChiAm(dd,mm,yy,dL,mL,yL,ll){
    var dayfull = canDay(dd,mm,yy) + " " + chiDay(dd,mm,yy);
    var monthFull = canMonth(mL,yL) + " " + chiMonth(mL) + "-" + testMoon(dd,mm,yy,ll);
    var yearFull = canYear(yL) + " " + chiYear(yL);
    return new Array(dayfull,monthFull,yearFull);
}
////////// them///////////////
function testNamNhuan(yyyy){
    var jd1 = getLunarMonth11(yyyy-1,TZ);
    var jd2 = getLunarMonth11(yyyy,TZ);
    if( (jd2 - jd1) > 365 ){
        var nhuan = getLeapMonthOffset(jd1,TZ) - 2;
        if(nhuan <= 0) nhuan = nhuan + 12;
        return nhuan;
    }
    else return -10;
}
function testM_full(dd,mm,yy){
    var jd = jdFromDate(dd,mm,yy);
    var dau1 = dauThangAm(jd);
    var dau2 = dau1+45;
    dau2 = dauThangAm(dau2);
    var hieu = dau2-dau1;
    if(hieu == 29)
        return false;
    else if(hieu == 30)
        return true;
}
function testMoon(dd,mm,yy,nhuan){
    str = "";
    if(nhuan == 1)
        str = "nhuận - ";
    var check = testM_full(dd,mm,yy);
    if(check == false)
        str += "thiếu";
    else str += "đủ";
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