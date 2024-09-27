import React from "react";

export function Table({ children }) {
  return <table>{children}</table>;
}

export function TableBody({ children }) {
  return <tbody>{children}</tbody>;
}

export function TableCell({ children }) {
  return <td>{children}</td>;
}

export function TableHead({ children }) {
  return <th>{children}</th>;
}

export function TableHeader({ children }) {
  return <thead>{children}</thead>;
}

export function TableRow({ children }) {
  return <tr>{children}</tr>;
}
