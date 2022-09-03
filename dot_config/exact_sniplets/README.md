# Sniplets

Each file in this directory with a `.snip` extension is loaded as a sniplet.

Files may containg the following:

- Empty lines are ignored.
- Lines whose first non-whitespace character is `#` are comments are ignored.
- Lines of the form

  ```
  keyword [keyword ...] sniplet
  ```

  form a sniplet. Keywords are used to identify a sniplet. Keywords and
  sniplets do not contain spaces.
