import { describe, expect, it } from "vitest";
import { validateVisualBaselinePaths } from "../../scripts/validate-visual-baseline-paths.mjs";

describe("visual baseline path allowlist", () => {
  it("accepts PNG snapshots under the approved Playwright directory", () => {
    expect(validateVisualBaselinePaths([
      "tests/visual/mockups.spec.mjs-snapshots/button-light-linux.png",
      "tests/visual/mockups.spec.mjs-snapshots/button-dark-linux.png",
      "packages/styles/tests/visual/mockups.spec.mjs-snapshots/button-light-linux.png",
    ])).toHaveLength(3);
  });

  it.each([
    ["outside directory", ["tests/unit/test.png"]],
    ["outside the styles package", ["packages/styles/package.json"]],
    ["monorepo path outside snapshots", ["packages/styles/tests/unit/test.png"]],
    ["directory traversal", ["tests/visual/mockups.spec.mjs-snapshots/../../package.json"]],
    ["wrong file type", ["tests/visual/mockups.spec.mjs-snapshots/README.md"]],
    ["empty changes", []],
  ])("rejects %s", (_case, paths) => {
    expect(() => validateVisualBaselinePaths(paths)).toThrow();
  });
});
