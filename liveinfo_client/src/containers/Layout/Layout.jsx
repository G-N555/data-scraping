import React, { Component } from "react";
import News from "../News/News";
import Area from "../../components/Area/Area";
import Genre from "../../components/Genre/Genre";
import SearchBar from "../../components/UI/SearchBar";

class Layout extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div>
        <News />
        <SearchBar />
        <Area />
        <Genre />
      </div>
    );
  }
}

export default Layout;
