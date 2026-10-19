/**
 * fiqhboard — comparative fiqh of the four Sunni schools.
 *
 * This is a placeholder release: it reserves the package name and exposes
 * version information only. It will become the client of the fiqhboard web
 * API; the logic itself stays in the Python core, never rewritten here.
 */

export const version = "0.0.1";
export const name = "fiqhboard";

/** Returns basic package information. */
export function info() {
  return {
    name,
    version,
    dataLoaded: false,
    homepage: "https://github.com/bayramkotan/fiqhboard",
  };
}
