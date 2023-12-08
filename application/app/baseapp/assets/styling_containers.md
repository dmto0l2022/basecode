#wrapper {  /* ADDED */
  position: relative;
  width: 200px;
}

#scrollable {
  height: 100px;
  border: 1px solid;
  overflow: auto;
  position: relative;
}

#wrapperFooter {
  background: red;
  position: absolute; /**/
  bottom:0;
}

<div id="wrapper">
  <div id="scrollable">
    <p style="border: 4px dashed #000; height: 200px;"></p>
  </div>
  <div id="wrapperFooter">ABSOLUTELY! :)</div>
</div>

