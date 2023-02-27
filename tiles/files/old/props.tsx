<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.2" tiledversion="1.3.0" name="props" tilewidth="30" tileheight="30" tilecount="81" columns="9">
 <image source="../props.png" width="270" height="270"/>
 <tile id="0">
  <properties>
   <property name="TYPE" value="color"/>
   <property name="COLOR" type="int" value="0"/>
  </properties>
  <animation>
   <frame tileid="0" duration="400"/>
   <frame tileid="9" duration="400"/>
   <frame tileid="18" duration="400"/>
   <frame tileid="27" duration="400"/>
   <frame tileid="36" duration="400"/>
   <frame tileid="45" duration="400"/>
   <frame tileid="54" duration="400"/>
  </animation>
 </tile>
 <tile id="1">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="2">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="3">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="4">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="5">
  <properties>
   <property name="TYPE" value="jump"/>
   <property name="DIRECTION" type="int" value="0"/>
  </properties>
  <animation>
   <frame tileid="5" duration="400"/>
   <frame tileid="6" duration="400"/>
   <frame tileid="5" duration="400"/>
   <frame tileid="14" duration="400"/>
   <frame tileid="15" duration="400"/>
   <frame tileid="14" duration="400"/>
   <frame tileid="5" duration="400"/>
   <frame tileid="6" duration="400"/>
   <frame tileid="5" duration="400"/>
  </animation>
 </tile>
 <tile id="6">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="7">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="8">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="9">
  <properties>
   <property name="TYPE" value="color"/>
   <property name="COLOR" type="int" value="1"/>
  </properties>
  <animation>
   <frame tileid="0" duration="400"/>
   <frame tileid="9" duration="400"/>
   <frame tileid="18" duration="400"/>
   <frame tileid="27" duration="400"/>
   <frame tileid="36" duration="400"/>
   <frame tileid="45" duration="400"/>
   <frame tileid="54" duration="400"/>
  </animation>
 </tile>
 <tile id="10">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="11">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="12">
  <properties>
   <property name="TYPE" value="metal"/>
  </properties>
 </tile>
 <tile id="13">
  <properties>
   <property name="TYPE" value="metal"/>
  </properties>
 </tile>
 <tile id="14">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="15">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="16">
  <properties>
   <property name="TYPE" value="destroy"/>
  </properties>
  <animation>
   <frame tileid="16" duration="400"/>
   <frame tileid="7" duration="400"/>
  </animation>
 </tile>
 <tile id="17">
  <properties>
   <property name="TYPE" value="carry"/>
  </properties>
  <animation>
   <frame tileid="17" duration="400"/>
   <frame tileid="8" duration="400"/>
  </animation>
 </tile>
 <tile id="18">
  <properties>
   <property name="TYPE" value="color"/>
   <property name="COLOR" type="int" value="2"/>
  </properties>
  <animation>
   <frame tileid="0" duration="400"/>
   <frame tileid="9" duration="400"/>
   <frame tileid="18" duration="400"/>
   <frame tileid="27" duration="400"/>
   <frame tileid="36" duration="400"/>
   <frame tileid="45" duration="400"/>
   <frame tileid="54" duration="400"/>
  </animation>
 </tile>
 <tile id="19">
  <properties>
   <property name="DIRECTION" type="int" value="1"/>
   <property name="TYPE" value="treadmill"/>
  </properties>
  <animation>
   <frame tileid="1" duration="400"/>
   <frame tileid="2" duration="400"/>
   <frame tileid="3" duration="400"/>
   <frame tileid="4" duration="400"/>
   <frame tileid="10" duration="400"/>
   <frame tileid="11" duration="400"/>
  </animation>
 </tile>
 <tile id="20">
  <properties>
   <property name="DIRECTION" type="int" value="3"/>
   <property name="TYPE" value="treadmill"/>
  </properties>
  <animation>
   <frame tileid="1" duration="400"/>
   <frame tileid="2" duration="400"/>
   <frame tileid="3" duration="400"/>
   <frame tileid="4" duration="400"/>
   <frame tileid="10" duration="400"/>
   <frame tileid="11" duration="400"/>
  </animation>
 </tile>
 <tile id="21">
  <properties>
   <property name="DIRECTION" type="int" value="5"/>
   <property name="TYPE" value="treadmill"/>
  </properties>
  <animation>
   <frame tileid="1" duration="400"/>
   <frame tileid="2" duration="400"/>
   <frame tileid="3" duration="400"/>
   <frame tileid="4" duration="400"/>
   <frame tileid="10" duration="400"/>
   <frame tileid="11" duration="400"/>
  </animation>
 </tile>
 <tile id="22">
  <properties>
   <property name="DIRECTION" type="int" value="7"/>
   <property name="TYPE" value="treadmill"/>
  </properties>
  <animation>
   <frame tileid="1" duration="400"/>
   <frame tileid="2" duration="400"/>
   <frame tileid="3" duration="400"/>
   <frame tileid="4" duration="400"/>
   <frame tileid="10" duration="400"/>
   <frame tileid="11" duration="400"/>
  </animation>
 </tile>
 <tile id="23">
  <properties>
   <property name="PRESS" type="int" value="0"/>
   <property name="TYPE" value="button"/>
  </properties>
  <animation>
   <frame tileid="23" duration="400"/>
   <frame tileid="24" duration="400"/>
  </animation>
 </tile>
 <tile id="24">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="25">
  <properties>
   <property name="DIRECTION" type="int" value="6"/>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="26">
  <properties>
   <property name="DIRECTION" type="int" value="8"/>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="27">
  <properties>
   <property name="TYPE" value="color"/>
   <property name="COLOR" type="int" value="3"/>
  </properties>
  <animation>
   <frame tileid="0" duration="400"/>
   <frame tileid="9" duration="400"/>
   <frame tileid="18" duration="400"/>
   <frame tileid="27" duration="400"/>
   <frame tileid="36" duration="400"/>
   <frame tileid="45" duration="400"/>
   <frame tileid="54" duration="400"/>
  </animation>
 </tile>
 <tile id="28">
  <properties>
   <property name="DIRECTION" type="int" value="1"/>
   <property name="TYPE" value="moving"/>
  </properties>
  <animation>
   <frame tileid="12" duration="400"/>
  </animation>
 </tile>
 <tile id="29">
  <properties>
   <property name="DIRECTION" type="int" value="3"/>
   <property name="TYPE" value="moving"/>
  </properties>
  <animation>
   <frame tileid="12" duration="400"/>
  </animation>
 </tile>
 <tile id="30">
  <properties>
   <property name="TYPE" value="colision"/>
  </properties>
 </tile>
 <tile id="31">
  <properties>
   <property name="TYPE" value="invisible"/>
  </properties>
 </tile>
 <tile id="32">
  <properties>
   <property name="PRESS" type="int" value="1"/>
   <property name="TYPE" value="button"/>
  </properties>
  <animation>
   <frame tileid="32" duration="400"/>
   <frame tileid="33" duration="400"/>
  </animation>
 </tile>
 <tile id="33">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="34">
  <properties>
   <property name="DIRECTION" type="int" value="2"/>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="35">
  <properties>
   <property name="DIRECTION" type="int" value="4"/>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="36">
  <properties>
   <property name="TYPE" value="color"/>
   <property name="COLOR" type="int" value="4"/>
  </properties>
  <animation>
   <frame tileid="0" duration="400"/>
   <frame tileid="9" duration="400"/>
   <frame tileid="18" duration="400"/>
   <frame tileid="27" duration="400"/>
   <frame tileid="36" duration="400"/>
   <frame tileid="45" duration="400"/>
   <frame tileid="54" duration="400"/>
  </animation>
 </tile>
 <tile id="37">
  <properties>
   <property name="GO" type="int" value="0"/>
   <property name="TYPE" value="portal"/>
  </properties>
  <animation>
   <frame tileid="37" duration="400"/>
   <frame tileid="46" duration="400"/>
   <frame tileid="55" duration="400"/>
   <frame tileid="64" duration="400"/>
  </animation>
 </tile>
 <tile id="38">
  <properties>
   <property name="GO" type="int" value="1"/>
   <property name="TYPE" value="portal"/>
  </properties>
  <animation>
   <frame tileid="38" duration="400"/>
   <frame tileid="47" duration="400"/>
   <frame tileid="56" duration="400"/>
   <frame tileid="65" duration="400"/>
  </animation>
 </tile>
 <tile id="39">
  <properties>
   <property name="TYPE" value="spike"/>
   <property name="WAIT" type="int" value="1"/>
  </properties>
  <animation>
   <frame tileid="39" duration="400"/>
   <frame tileid="48" duration="400"/>
   <frame tileid="57" duration="400"/>
   <frame tileid="66" duration="400"/>
  </animation>
 </tile>
 <tile id="40">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="41">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="42">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="43">
  <properties>
   <property name="DIRECTION" value="hor"/>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="44">
  <properties>
   <property name="DIRECTION" value="ver"/>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="45">
  <properties>
   <property name="TYPE" value="color"/>
   <property name="COLOR" type="int" value="5"/>
  </properties>
  <animation>
   <frame tileid="0" duration="400"/>
   <frame tileid="9" duration="400"/>
   <frame tileid="18" duration="400"/>
   <frame tileid="27" duration="400"/>
   <frame tileid="36" duration="400"/>
   <frame tileid="45" duration="400"/>
   <frame tileid="54" duration="400"/>
  </animation>
 </tile>
 <tile id="46">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="47">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="48">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="49">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="50">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="51">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="52">
  <properties>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="53">
  <properties>
   <property name="TYPE" value="tunnel"/>
  </properties>
 </tile>
 <tile id="54">
  <properties>
   <property name="TYPE" value="color"/>
   <property name="COLOR" type="int" value="6"/>
  </properties>
  <animation>
   <frame tileid="0" duration="400"/>
   <frame tileid="9" duration="400"/>
   <frame tileid="18" duration="400"/>
   <frame tileid="27" duration="400"/>
   <frame tileid="36" duration="400"/>
   <frame tileid="45" duration="400"/>
   <frame tileid="54" duration="400"/>
  </animation>
 </tile>
 <tile id="55">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="56">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="57">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="58">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="59">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="60">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="61">
  <properties>
   <property name="TYPE" value="lever"/>
   <property name="VALUE" type="int" value="0"/>
  </properties>
  <animation>
   <frame tileid="52" duration="400"/>
   <frame tileid="61" duration="400"/>
  </animation>
 </tile>
 <tile id="62">
  <properties>
   <property name="TYPE" value="light"/>
   <property name="VALUE" type="int" value="0"/>
  </properties>
  <animation>
   <frame tileid="53" duration="400"/>
   <frame tileid="62" duration="400"/>
  </animation>
 </tile>
 <tile id="63">
  <properties>
   <property name="TYPE" value="hole"/>
  </properties>
 </tile>
 <tile id="64">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="65">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="66">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="67">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="68">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="69">
  <properties>
   <property name="TYPE" value="wall"/>
  </properties>
 </tile>
 <tile id="70">
  <properties>
   <property name="TYPE" value="lever"/>
   <property name="VALUE" type="int" value="1"/>
  </properties>
  <animation>
   <frame tileid="52" duration="400"/>
   <frame tileid="61" duration="400"/>
  </animation>
 </tile>
 <tile id="71">
  <properties>
   <property name="TYPE" value="light"/>
   <property name="VALUE" type="int" value="1"/>
  </properties>
  <animation>
   <frame tileid="53" duration="400"/>
   <frame tileid="62" duration="400"/>
  </animation>
 </tile>
 <tile id="72">
  <properties>
   <property name="TYPE" value="spike"/>
   <property name="WAIT" type="int" value="0"/>
  </properties>
  <animation>
   <frame tileid="72" duration="400"/>
  </animation>
 </tile>
 <tile id="73">
  <properties>
   <property name="TYPE" value="slime"/>
  </properties>
 </tile>
 <tile id="74">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="75">
  <properties>
   <property name="TYPE" value="none"/>
  </properties>
 </tile>
 <tile id="76">
  <properties>
   <property name="TYPE" value="door"/>
  </properties>
  <animation>
   <frame tileid="76" duration="400"/>
   <frame tileid="77" duration="400"/>
   <frame tileid="78" duration="400"/>
   <frame tileid="79" duration="400"/>
  </animation>
 </tile>
 <tile id="77">
  <properties>
   <property name="TYPE" value="door"/>
  </properties>
 </tile>
 <tile id="78">
  <properties>
   <property name="TYPE" value="door"/>
  </properties>
 </tile>
 <tile id="79">
  <properties>
   <property name="TYPE" value="door"/>
  </properties>
 </tile>
</tileset>
