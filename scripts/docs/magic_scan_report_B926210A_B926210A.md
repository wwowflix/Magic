# MAGIC Project Scan Report

> Generated: 2025-09-11 20:35:57

## Summary
- **ruff:** [FAIL] (exit 2)
- **black --check:** [FAIL] (exit 1)
- **mypy:** [FAIL] (exit 2)
- **bandit:** [FAIL] (exit 2)
- **detect-secrets:** [OK] (exit 0)
- **pip-audit:** [OK] (exit 0)

## Detailed Results
### ruff
**stderr:**
``\nRuff: An extremely fast Python linter and code formatter.

Usage: ruff [OPTIONS] <COMMAND>

Commands:
  check    Run Ruff on the given files or directories
  rule     Explain a rule (or all rules)
  config   List or describe the available configuration options
  linter   List all supported upstream linters
  clean    Clear any caches in the current directory and any subdirectories
  format   Run the Ruff formatter on the given files or directories
  server   Run the language server
  analyze  Run analysis over Python source code
  version  Display Ruff's version
  help     Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version

Log levels:
  -v, --verbose  Enable verbose logging
  -q, --quiet    Print diagnostics, but nothing else
  -s, --silent   Disable all logging (but still exit with status code "1" upon detecting
                 diagnostics)

Global options:
      --config <CONFIG_OPTION>  Either a path to a TOML configuration file (`pyproject.toml` or
                                `ruff.toml`), or a TOML `<KEY> = <VALUE>` pair (such as you might
                                find in a `ruff.toml` configuration file) overriding a specific
                                configuration option. Overrides of individual settings using this
                                option always take precedence over all configuration files,
                                including configuration files that were also specified using
                                `--config`
      --isolated                Ignore all configuration files

For help with a specific command, see: `ruff help <command>`.\n``

### black --check
**stderr:**
``\nUsage: black [OPTIONS] SRC ...

One of 'SRC' or 'code' is required.\n``

### mypy
**stderr:**
``\nusage: mypy [-h] [-v] [-V] [more options; see below]
            [-m MODULE] [-p PACKAGE] [-c PROGRAM_TEXT] [files ...]
mypy: error: Missing target module, package, files, or command.\n``

### bandit
``\nusage: bandit [-h] [-r] [-a {file,vuln}] [-n CONTEXT_LINES] [-c CONFIG_FILE]
              [-p PROFILE] [-t TESTS] [-s SKIPS] [-l |
              --severity-level {all,low,medium,high}] [-i |
              --confidence-level {all,low,medium,high}]
              [-f {csv,custom,html,json,screen,txt,xml,yaml}]
              [--msg-template MSG_TEMPLATE] [-o [OUTPUT_FILE]] [-v] [-d] [-q]
              [--ignore-nosec] [-x EXCLUDED_PATHS] [-b BASELINE]
              [--ini INI_PATH] [--exit-zero] [--version]
              [targets ...]\n``

### detect-secrets
``\nusage: detect-secrets [-h] [-v] [--version] [-C <path>] [-c NUM_CORES]
                      {scan,audit} ...

positional arguments:
  {scan,audit}
    scan                Creates a baseline by scanning a repository for
                        secrets.
    audit               Manually assesses a baseline to determine validity of
                        secrets found.

options:
  -h, --help            show this help message and exit
  -v, --verbose         Verbose mode.
  --version             Display version information.
  -C <path>             Run as if detect-secrets was started in <path>, rather
                        than in the current working directory.
  -c, --cores NUM_CORES
                        Specify the number of cores to use for parallel
                        processing. Defaults to using the max cores on the
                        current host.\n``

### pip-audit
**stderr:**
``\nNo known vulnerabilities found\n``

## Heuristics (quick flags)
### Bare except
- (none)

### Ambiguous single-letter l vars
- scripts/C_B_D_T_.py
- scripts/C_P_A_L_.py
- scripts/D_S_I_G_.py
- scripts/E_B_L_C_.py
- scripts/F__e_a_t.py
- scripts/G_M_A_P_.py
- scripts/G__l_a_t.py
- scripts/M_E_T_A_.py
- scripts/MacRoman.py
- scripts/O_S_2f_2.py
- scripts/S_V_G_.py
- scripts/S__i_l_f.py
- scripts/StandardEncoding.py
- scripts/__init___136.py
- scripts/__init___153.py
- scripts/__init___163.py
- scripts/__init___168.py
- scripts/__init___171.py
- scripts/__init___40.py
- scripts/__init___45.py
- scripts/__init___86.py
- scripts/_abnf.py
- scripts/_add_newdocs.py
- scripts/_c_m_a_p.py
- scripts/_char_codes.py
- scripts/_connection.py
- scripts/_core.py
- scripts/_doctools.py
- scripts/_f_v_a_r.py
- scripts/_g_l_y_f.py
- scripts/_g_v_a_r.py
- scripts/_h_d_m_x.py
- scripts/_h_e_a_d.py
- scripts/_h_h_e_a.py
- scripts/_impl.py
- scripts/_internal.py
- scripts/_iotools.py
- scripts/_k_e_r_n.py
- scripts/_l_o_c_a.py
- scripts/_m_e_t_a.py
- scripts/_p_o_s_t.py
- scripts/_parser_2.py
- scripts/_polybase.py
- scripts/_pytesttester.py
- scripts/_s_b_i_x.py
- scripts/_subprocess.py
- scripts/_t_r_a_k.py
- scripts/_tokenizer.py
- scripts/_v_h_e_a.py
- scripts/absoft.py
- scripts/actions.py
- scripts/afmLib.py
- scripts/agl.py
- scripts/ast.py
- scripts/ast_2.py
- scripts/asyn.py
- scripts/auxfuncs.py
- scripts/bcppcompiler.py
- scripts/bdist_rpm.py
- scripts/bench.py
- scripts/bidi.py
- scripts/build_ext.py
- scripts/build_src.py
- scripts/builder_3.py
- scripts/builder_4.py
- scripts/builder_5.py
- scripts/c_lexer.py
- scripts/c_parser.py
- scripts/cached.py
- scripts/caching.py
- scripts/capi_maps.py
- scripts/ccompiler.py
- scripts/ccompiler_opt.py
- scripts/cfuncs.py
- scripts/chardetect.py
- scripts/chebyshev.py
- scripts/cmdline.py
- scripts/common.py
- scripts/config.py
- scripts/config_compiler.py
- scripts/config_init.py
- scripts/config_init_2.py
- scripts/constant.py
- scripts/constant_2.py
- scripts/converter.py
- scripts/core.py
- scripts/core_2.py
- scripts/cpp.py
- scripts/cpuinfo.py
- scripts/crackfortran.py
- scripts/css_match.py
- scripts/ctokens.py
- scripts/cu2qu.py
- scripts/doctestcompare.py
- scripts/drawing.py
- scripts/easy_install.py
- scripts/ext.py
- scripts/extension.py
- scripts/extras.py
- scripts/f2py2e.py
- scripts/f2py_testing.py
- scripts/facebook.py
- scripts/fallback.py
- scripts/fancy_getopt.py
- scripts/featureVars.py
- scripts/filenames.py
- scripts/filenames_2.py
- scripts/fonts.py
- scripts/fpdf.py
- scripts/frame.py
- scripts/freetypePen.py
- scripts/frequencies.py
- scripts/from_template.py
- scripts/ftp.py
- scripts/func2subr.py
- scripts/fuse.py
- scripts/generic.py
- scripts/grUtils.py
- scripts/gui.py
- scripts/helpers.py
- scripts/hermite.py
- scripts/hermite_e.py
- scripts/html_2.py
- scripts/http.py
- scripts/http_sync.py
- scripts/ibm.py
- scripts/image.py
- scripts/image_parsing.py
- scripts/inference.py
- scripts/install_clib.py
- scripts/interpolatableHelpers.py
- scripts/interpolate_layout.py
- scripts/iup.py
- scripts/laguerre.py
- scripts/langbulgarianmodel.py
- scripts/langgreekmodel.py
- scripts/langhebrewmodel.py
- scripts/langhungarianmodel.py
- scripts/langrussianmodel.py
- scripts/langthaimodel.py
- scripts/langturkishmodel.py
- scripts/legendre.py
- scripts/lextab.py
- scripts/linalg.py
- scripts/line_break.py
- scripts/linearization.py
- scripts/list.py
- scripts/macRes.py
- scripts/markers.py
- scripts/melt.py
- scripts/merger.py
- scripts/mingw32ccompiler.py
- scripts/misc_util.py
- scripts/model_3.py
- scripts/modeline.py
- scripts/models_3.py
- scripts/more.py
- scripts/msvc9compiler.py
- scripts/msvccompiler.py
- scripts/name.py
- scripts/npy_pkg_config.py
- scripts/numerictypes.py
- scripts/otBase.py
- scripts/otConverters.py
- scripts/otTables.py
- scripts/outline.py
- scripts/palette.py
- scripts/parser_3.py
- scripts/parser_4.py
- scripts/phase0/module_L/0L_placeholder_READY.py
- scripts/phase06/module_L/06L_analytics_pull_sync_READY.py
- scripts/phase06/module_L/06L_upload_cost_logger_READY.py
- scripts/phase08/module_L/08L_push_thumbnail_insights_to_prism_READY.py
- scripts/phase08/module_L/08L_recommend_posting_time_updates_READY.py
- scripts/phase08/module_L/08L_update_scribe_generation_prompts_READY.py
- scripts/phase1/module_L/1L_placeholder_READY.py
- scripts/phase10/module_L/10L_historical_seo_tracker_READY.py
- scripts/phase10/module_L/10L_placeholder_READY.py
- scripts/phase10/module_L/10L_platform_roi_comparer_READY.py
- scripts/phase10/module_L/10L_seo_forecast_engine_READY.py
- scripts/phase12/module_L/12L_agent_collaboration_bridge_READY.py
- scripts/phase12/module_L/12L_comment_thread_mapper_READY.py
- scripts/phase12/module_L/12L_feedback_notification_bot_READY.py
- scripts/phase12/module_L/12L_notifier_for_viral_ugc_spikes_READY.py
- scripts/phase12/module_L/12L_placeholder_READY.py
- scripts/phase13/module_L/13L_affiliate_lead_memory_graph_READY.py
- scripts/phase13/module_L/13L_affiliate_purchase_attribution_READY.py
- scripts/phase13/module_L/13L_crm_event_replayer_READY.py
- scripts/phase13/module_L/13L_funnel_abandonment_re_engager_READY.py
- scripts/phase13/module_L/13L_placeholder_READY.py
- scripts/phase14/module_L/14L_adaptive_decision_refiner_READY.py
- scripts/phase14/module_L/14L_agent_performance_feedback_loop_READY.py
- scripts/phase14/module_L/14L_llm_choice_rebalancer_READY.py
- scripts/phase14/module_L/14L_placeholder_READY.py
- scripts/phase15/module_L/15L_placeholder_READY.py
- scripts/phase16/module_L/16L_placeholder_READY.py
- scripts/phase17/module_L/17L_placeholder_READY.py
- scripts/phase18/module_L/18L_customer_ltv_estimator_READY.py
- scripts/phase18/module_L/18L_forecasting_ai_30_90_180_days__READY.py
- scripts/phase18/module_L/18L_funnel_drop_off_analyzer_READY.py
- scripts/phase18/module_L/18L_placeholder_READY.py
- scripts/phase2/module_L/2L_placeholder_READY.py
- scripts/phase3/module_L/3L_placeholder_READY.py
- scripts/phase4/module_L/4L_placeholder_READY.py
- scripts/phase5/module_L/5L_placeholder_READY.py
- scripts/phase6/module_L/6L_placeholder_READY.py
- scripts/phase7/module_L/7L_placeholder_READY.py
- scripts/phase8/module_L/8L_placeholder_READY.py
- scripts/phase9/module_L/9L_placeholder_READY.py
- scripts/pkgconfig.py
- scripts/pkgconfig_2.py
- scripts/polynomial_2.py
- scripts/polyutils.py
- scripts/print_coercion_tables.py
- scripts/psCharStrings.py
- scripts/pwa.py
- scripts/python.py
- scripts/python_parser.py
- scripts/recipes.py
- scripts/records.py
- scripts/relativedelta.py
- scripts/relativedelta_2.py
- scripts/requirements.py
- scripts/rrule.py
- scripts/rrule_2.py
- scripts/rules.py
- scripts/sas7bdat.py
- scripts/sbixStrike.py
- scripts/setup_3.py
- scripts/setup_common.py
- scripts/sfnt.py
- scripts/shape_base_2.py
- scripts/shapes.py
- scripts/shell_completion.py
- scripts/spec.py
- scripts/specializer.py
- scripts/ssh.py
- scripts/sstruct.py
- scripts/stancsv.py
- scripts/standardGlyphOrder.py
- scripts/statNames.py
- scripts/stata.py
- scripts/style_render.py
- scripts/svgPathPen.py
- scripts/syntax.py
- scripts/sysconfig.py
- scripts/template.py
- scripts/test_api.py
- scripts/test_array_coercion.py
- scripts/test_build.py
- scripts/test_casting_unittests.py
- scripts/test_config.py
- scripts/test_cpu_features.py
- scripts/test_defchararray.py
- scripts/test_dt_accessor.py
- scripts/test_dtype.py
- scripts/test_f2py2e.py
- scripts/test_fiscal.py
- scripts/test_frame_legend.py
- scripts/test_function_base.py
- scripts/test_function_base_2.py
- scripts/test_generator_mt19937.py
- scripts/test_generator_nested.py
- scripts/test_greenlet.py
- scripts/test_header.py
- scripts/test_io.py
- scripts/test_linalg.py
- scripts/test_mrecords.py
- scripts/test_npy_pkg_config.py
- scripts/test_numerictypes.py
- scripts/test_numpy.py
- scripts/test_parsing.py
- scripts/test_period_asfreq.py
- scripts/test_period_index.py
- scripts/test_pivot.py
- scripts/test_pocketfft.py
- scripts/test_random.py
- scripts/test_randomstate.py
- scripts/test_randomstate_regression.py
- scripts/test_reset_index.py
- scripts/test_return_complex.py
- scripts/test_return_integer.py
- scripts/test_return_logical.py
- scripts/test_return_real.py
- scripts/test_scalarbuffer.py
- scripts/test_scalarmath.py
- scripts/test_stack_unstack.py
- scripts/test_stata.py
- scripts/test_stringdtype.py
- scripts/test_sync.py
- scripts/test_textreader.py
- scripts/test_timedelta_range.py
- scripts/test_to_dict.py
- scripts/test_to_latex.py
- scripts/test_twodim_base.py
- scripts/test_ufunc.py
- scripts/test_umath.py
- scripts/test_utils_2.py
- scripts/textTools.py
- scripts/text_region.py
- scripts/tfmLib.py
- scripts/timedeltas.py
- scripts/token.py
- scripts/transforms_2.py
- scripts/ttProgram.py
- scripts/ttfonts.py
- scripts/ttx.py
- scripts/twitter.py
- scripts/type_check.py
- scripts/tz.py
- scripts/tz_2.py
- scripts/ufo.py
- scripts/unixccompiler.py
- scripts/util_2.py
- scripts/util_3.py
- scripts/util_4.py
- scripts/utils_6.py
- scripts/uts46data.py
- scripts/variableScalar.py
- scripts/verifier.py
- scripts/verifier_2.py
- scripts/voltToFea.py
- scripts/woff2.py
- scripts/x_user_defined.py
- scripts/xmlReader.py
- scripts/yacc.py

### eval/exec usage
- scripts/M_E_T_A_.py
- scripts/S_I_N_G_.py
- scripts/__init___153.py
- scripts/_inputstream.py
- scripts/_io_epoll.py
- scripts/_make.py
- scripts/_make_2.py
- scripts/arrayprint.py
- scripts/auxfuncs.py
- scripts/build_meta.py
- scripts/capi_maps.py
- scripts/ccompiler.py
- scripts/cpp.py
- scripts/crackfortran.py
- scripts/eval.py
- scripts/execeval.py
- scripts/f2py_testing.py
- scripts/frame.py
- scripts/functools.py
- scripts/launch.py
- scripts/lex.py
- scripts/lstm_forecast_torch_2.py
- scripts/misc_util.py
- scripts/otBase.py
- scripts/otConverters.py
- scripts/otTables.py
- scripts/overrides.py
- scripts/parameterized.py
- scripts/recompiler.py
- scripts/recompiler_2.py
- scripts/results.py
- scripts/runtime.py
- scripts/sandbox.py
- scripts/setuptools_build.py
- scripts/setuptools_ext.py
- scripts/setuptools_ext_2.py
- scripts/six.py
- scripts/six_2.py
- scripts/symfont.py
- scripts/test_arrayprint.py
- scripts/test_category.py
- scripts/test_ccompiler_opt.py
- scripts/test_compat.py
- scripts/test_dtype.py
- scripts/test_eval.py
- scripts/test_finalize.py
- scripts/test_methods.py
- scripts/test_old_base.py
- scripts/test_public_api.py
- scripts/test_query_eval.py
- scripts/test_range.py
- scripts/test_records.py
- scripts/test_rendering.py
- scripts/test_scalarmath.py
- scripts/test_simd.py
- scripts/test_testing_raisesgroup.py
- scripts/test_umath.py
- scripts/test_umath_accuracy.py
- scripts/threadpoolctl.py
- scripts/timer_comparison.py
- scripts/to_interpreter.py
- scripts/typing_extensions.py
- scripts/typing_extensions_2.py
- scripts/utils_6.py
- scripts/yacc.py

### subprocess shell=True
- (none)

### Wildcard imports
- scripts/G__l_a_t.py
- scripts/S__i_l_f.py
- scripts/__init___12.py
- scripts/__init___139.py
- scripts/__init___155.py
- scripts/__init___156.py
- scripts/__init___167.py
- scripts/__init___168.py
- scripts/__init___172.py
- scripts/__init___174.py
- scripts/__init___175.py
- scripts/__init___33.py
- scripts/__init___34.py
- scripts/__init___36.py
- scripts/__init___38.py
- scripts/__init___45.py
- scripts/__init___47.py
- scripts/__init___49.py
- scripts/__init___51.py
- scripts/__init___53.py
- scripts/__init___57.py
- scripts/__init___60.py
- scripts/__init___72.py
- scripts/__init___85.py
- scripts/__init___90.py
- scripts/__init___91.py
- scripts/__init___92.py
- scripts/__main___19.py
- scripts/_config_3.py
- scripts/_http.py
- scripts/_imp_emulation.py
- scripts/_imp_emulation_2.py
- scripts/_run.py
- scripts/_state.py
- scripts/api_7.py
- scripts/arrayprint.py
- scripts/benchmark.py
- scripts/benchmark_2.py
- scripts/builder_2.py
- scripts/capi_maps.py
- scripts/channels.py
- scripts/common.py
- scripts/converters_2.py
- scripts/converters_4.py
- scripts/core.py
- scripts/core_7.py
- scripts/crackfortran.py
- scripts/decorators.py
- scripts/errors.py
- scripts/etree_3.py
- scripts/etree_4.py
- scripts/exceptions_2.py
- scripts/exceptions_5.py
- scripts/f90mod_rules.py
- scripts/filters_2.py
- scripts/filters_4.py
- scripts/helpers.py
- scripts/interpolatable.py
- scripts/interpolatablePlot.py
- scripts/interpolatableTestContourOrder.py
- scripts/interpolatableTestStartingPoint.py
- scripts/isympy.py
- scripts/iterTools.py
- scripts/log_2.py
- scripts/matlib.py
- scripts/mixins_2.py
- scripts/multiarray.py
- scripts/pointPen_2.py
- scripts/pylab.py
- scripts/recompiler.py
- scripts/recompiler_2.py
- scripts/reddit_scraper_2.py
- scripts/setters_2.py
- scripts/setters_4.py
- scripts/setup_3.py
- scripts/tables.py
- scripts/test_highlevel_socket.py
- scripts/test_reddit_2.py
- scripts/test_reddit_login_2.py
- scripts/test_secrets_2.py
- scripts/test_sync.py
- scripts/test_testing.py
- scripts/tz.py
- scripts/tz_2.py
- scripts/tzwin.py
- scripts/tzwin_2.py
- scripts/umath.py
- scripts/umath_tests.py
- scripts/utils_5.py
- scripts/validators_2.py
- scripts/validators_4.py

### Hardcoded password/token
- scripts/_config_2.py
- scripts/_http.py
- scripts/_oid.py
- scripts/_serialization.py
- scripts/adapters.py
- scripts/auth.py
- scripts/client_config.py
- scripts/connectionpool.py
- scripts/dist.py
- scripts/encryption.py
- scripts/fpdf.py
- scripts/ftp.py
- scripts/fuse.py
- scripts/index.py
- scripts/json_2.py
- scripts/load_secret_test.py
- scripts/low_level.py
- scripts/misc.py
- scripts/network.py
- scripts/orchestrator.py
- scripts/package_index.py
- scripts/prompt.py
- scripts/pyopenssl.py
- scripts/reddit_api_2.py
- scripts/reddit_api_3.py
- scripts/reddit_api_final.py
- scripts/reddit_api_fixed.py
- scripts/reddit_check.py
- scripts/reddit_scraper_2.py
- scripts/reddit_test.py
- scripts/register.py
- scripts/save_api_key_2.py
- scripts/secrets_2.py
- scripts/securetransport.py
- scripts/sessions.py
- scripts/smb.py
- scripts/socks.py
- scripts/socks_2.py
- scripts/sockshandler.py
- scripts/sockshandler_2.py
- scripts/spec.py
- scripts/ssh.py
- scripts/subscribe_convertkit_2.py
- scripts/test_reddit.py
- scripts/test_reddit_2.py
- scripts/test_reddit_login_2.py
- scripts/trends_scraper_with_reddit.py
- scripts/upload.py
- scripts/vault_manager.py
- scripts/versioncontrol.py
- scripts/webhdfs.py
- scripts/youtube_api_2.py
